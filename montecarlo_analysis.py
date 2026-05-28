"""
Monte Carlo Analysis Pipeline for Station Nightclub ABM Evacuation Simulation

This script runs multiple simulation iterations, collects statistical metrics,
and performs comprehensive statistical analysis including:
- Sample statistics
- Confidence intervals
- Distribution fitting (MLE)
- Bootstrapping
- Visualization generation
- Heatmap analysis
- Markdown report generation

Usage:
    python montecarlo_analysis.py --scenario 1 --simulations 100
"""

import argparse
import os
import random
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from datetime import datetime

from config.scenarios import get_scenario
from config.constants import EXIT, FIRE
from data_io.loaders import cargar_layout, cargar_agentes
from simulation.fire import FireSimulation
from simulation.smoke import SmokeSimulation
from simulation.movement import mover, build_step_arrays
from metrics.collector import MetricsCollector

import copy
from joblib import Parallel, delayed


# =========================================================
# MONTE CARLO SIMULATION RUNNER
# =========================================================

class MonteCarloRunner:
    def __init__(self, scenario_num: int, num_simulations: int = 30):
        self.scenario_num = scenario_num
        self.num_simulations = num_simulations
        self.cfg = get_scenario(scenario_num)
        self.results = []

        # Load all CSVs once — shared as read-only templates.
        # Each simulation deepcopies these instead of hitting disk.
        print(f"Loading data for scenario {scenario_num}...")

        self._world_template = cargar_layout(
            os.path.join("data", "building_nightclub.csv"))
        self._world_template.calcular_interior()
        self._world_template.aplicar_blocked_exits(self.cfg["blocked_exits"])
        self._world_template.calcular_distance_maps()

        self._fire_template = FireSimulation()
        self._fire_template.cargar_eventos(
            os.path.join("data", "fire_nightclub_merged.csv"),
            self._world_template)

        self._smoke_template = SmokeSimulation()
        self._smoke_template.cargar_eventos(
            os.path.join("data", "smoke.csv"),
            self._world_template)

        self._agentes_template = cargar_agentes(
            os.path.join("data", "people.csv"),
            self._world_template, self.cfg)

        print("Data loaded. Ready to run simulations.")

    def run_single_simulation(self, seed: int) -> dict:
        random.seed(seed)
        np.random.seed(seed)

        # Deepcopy mutable state — no disk reads
        world     = copy.deepcopy(self._world_template)
        fire_sim  = copy.deepcopy(self._fire_template)
        smoke_sim = copy.deepcopy(self._smoke_template)
        agentes   = copy.deepcopy(self._agentes_template)

        metrics = MetricsCollector()
        escape_times = []
        window_escapes = 0
        position_history = []
        death_positions = []
        smoke_exposure = np.zeros((world.height, world.width), dtype=np.float32)

        steps = self.cfg["simulation_steps"]

        for t in range(steps):
            fire_sim.actualizar(world, t)
            fire_sim.expandir(world, t, self.cfg)

            smoke_sim.actualizar(world, t, self.cfg)

            smoke_exposure += world.smoke

            # Build step arrays once per step, update as agents move
            occupancy, fire_score = build_step_arrays(agentes, world)

            for a in agentes:
                if not a.alive:
                    continue

                position_history.append((a.x, a.y))

                old_x, old_y = a.x, a.y

                mover(a, agentes, world, t, occupancy, fire_score)

                if (a.x, a.y) != (old_x, old_y):
                    occupancy[old_y][old_x] -= 1
                    occupancy[a.y][a.x]     += 1

                densidad = world.smoke[a.y][a.x]
                a.smoke_inhaled += densidad * 0.22
                a.energy        -= densidad * 0.05

                if a.smoke_inhaled > 120 or a.energy < 45:
                    a.injured = True

                if world.grid[a.y][a.x] == FIRE:
                    a.alive = False
                    death_positions.append((a.x, a.y))

                elif world.grid[a.y][a.x] == EXIT:
                    a.evacuated = True
                    a.alive = False
                    escape_times.append(t)

                elif a.energy <= 0 or a.smoke_inhaled > 260:
                    a.alive = False
                    death_positions.append((a.x, a.y))

            metrics.record(t, agentes, world, occupancy)

        total_evacuated = sum(a.evacuated for a in agentes)
        total_dead      = sum((not a.alive) and (not a.evacuated) for a in agentes)
        total_injured   = sum(a.injured for a in agentes)
        total_trapped   = sum(a.alive for a in agentes)

        avg_escape_time = np.mean(escape_times) if escape_times else 0
        max_density     = max(metrics.avg_density) if metrics.avg_density else 0
        avg_smoke       = np.mean(metrics.avg_smoke) if metrics.avg_smoke else 0

        return {
            'simulation_id':        seed,
            'total_evacuated':      total_evacuated,
            'total_dead':           total_dead,
            'total_injured':        total_injured,
            'total_trapped':        total_trapped,
            'average_escape_time':  avg_escape_time,
            'max_density':          max_density,
            'average_smoke':        avg_smoke,
            'window_escape_count':  window_escapes,
            'total_simulation_time': steps,
            'position_history':     position_history,
            'death_positions':      death_positions,
            'smoke_exposure':       smoke_exposure,
            'escape_times':         escape_times
        }

    def run_all_simulations(self):
        print(f"\n{'='*60}")
        print(f"MONTE CARLO ANALYSIS - Scenario {self.scenario_num}")
        print(f"{'='*60}")
        print(f"Number of simulations: {self.num_simulations}")
        print(f"Configuration: {self.cfg['name']}")
        print(f"{'='*60}\n")

        seeds = list(range(1, self.num_simulations + 1))

        results = Parallel(n_jobs=-1, verbose=10)(
            delayed(self.run_single_simulation)(seed) for seed in seeds
        )

        self.results = [r for r in results if r is not None]
        print(f"\nCompleted {len(self.results)}/{self.num_simulations} simulations")
        return self.results

# =========================================================
# STATISTICAL ANALYSIS MODULES
# =========================================================

class StatisticalAnalyzer:
    """
    Performs statistical analysis on Monte Carlo results.
    """
    
    def __init__(self, results: list):
        self.results = results
        self.df = pd.DataFrame(results)
        
    def calculate_sample_statistics(self) -> pd.DataFrame:
        """
        Calculate sample statistics for all major metrics.
        """
        metrics = ['total_evacuated', 'total_dead', 'total_injured', 
                   'total_trapped', 'average_escape_time', 'max_density', 'average_smoke']
        
        stats_dict = {}
        
        for metric in metrics:
            data = self.df[metric].values
            stats_dict[metric] = {
                'mean': np.mean(data),
                'variance': np.var(data, ddof=1),
                'std_dev': np.std(data, ddof=1),
                'min': np.min(data),
                'max': np.max(data),
                'median': np.median(data),
                'q25': np.percentile(data, 25),
                'q75': np.percentile(data, 75)
            }
        
        return pd.DataFrame(stats_dict).T
    
    def calculate_confidence_intervals(self, confidence: float = 0.95) -> pd.DataFrame:
        """
        Calculate confidence intervals for key metrics.
        CI = mean ± z * (std / sqrt(n))
        """
        metrics = ['total_evacuated', 'total_dead', 'total_injured', 
                   'total_trapped', 'average_escape_time']
        
        z_score = stats.norm.ppf((1 + confidence) / 2)
        n = len(self.results)
        
        ci_dict = {}
        
        for metric in metrics:
            data = self.df[metric].values
            mean = np.mean(data)
            std = np.std(data, ddof=1)
            margin = z_score * (std / np.sqrt(n))
            
            ci_dict[metric] = {
                'mean': mean,
                'std': std,
                'margin_of_error': margin,
                'ci_lower': mean - margin,
                'ci_upper': mean + margin,
                'confidence_level': confidence
            }
        
        return pd.DataFrame(ci_dict).T
    
    def fit_distributions(self, metric: str) -> dict:
        """
        Fit Normal, Lognormal, and Weibull distributions using MLE.
        Returns parameters and goodness-of-fit metrics.
        """
        data = self.df[metric].values
        data = data[data > 0]  # Remove zeros for lognormal and Weibull
        
        if len(data) < 10:
            return None
        
        results = {}
        
        # Normal distribution
        try:
            norm_params = stats.norm.fit(data)
            log_lik = np.sum(stats.norm.logpdf(data, *norm_params))
            k = 2  # parameters
            results['normal'] = {
                'params': norm_params,
                'log_likelihood': log_lik,
                'aic': 2 * k - 2 * log_lik,
                'bic': k * np.log(len(data)) - 2 * log_lik
            }
        except:
            pass
        
        # Lognormal distribution
        try:
            lognorm_params = stats.lognorm.fit(data, floc=0)
            log_lik = np.sum(stats.lognorm.logpdf(data, *lognorm_params))
            k = 3  # parameters
            results['lognormal'] = {
                'params': lognorm_params,
                'log_likelihood': log_lik,
                'aic': 2 * k - 2 * log_lik,
                'bic': k * np.log(len(data)) - 2 * log_lik
            }
        except:
            pass
        
        # Weibull distribution
        try:
            weibull_params = stats.weibull_min.fit(data, floc=0)
            log_lik = np.sum(stats.weibull_min.logpdf(data, *weibull_params))
            k = 3  # parameters
            results['weibull'] = {
                'params': weibull_params,
                'log_likelihood': log_lik,
                'aic': 2 * k - 2 * log_lik,
                'bic': k * np.log(len(data)) - 2 * log_lik
            }
        except:
            pass
        
        # Determine best fit by AIC
        if results:
            best_fit = min(results.keys(), key=lambda x: results[x]['aic'])
            results['best_fit'] = best_fit
        
        return results
    
    def bootstrap_analysis(self, metric: str, n_bootstrap: int = 1000) -> dict:
        """
        Perform bootstrap resampling for a metric.
        """
        data = self.df[metric].values
        n = len(data)
        
        bootstrap_means = []
        bootstrap_samples = []
        
        for _ in range(n_bootstrap):
            sample = np.random.choice(data, size=n, replace=True)
            bootstrap_means.append(np.mean(sample))
            bootstrap_samples.append(sample)
        
        bootstrap_means = np.array(bootstrap_means)
        
        # Calculate bootstrap confidence intervals
        ci_lower = np.percentile(bootstrap_means, 2.5)
        ci_upper = np.percentile(bootstrap_means, 97.5)
        
        return {
            'original_mean': np.mean(data),
            'bootstrap_mean': np.mean(bootstrap_means),
            'bootstrap_std': np.std(bootstrap_means),
            'bootstrap_ci_lower': ci_lower,
            'bootstrap_ci_upper': ci_upper,
            'bootstrap_means': bootstrap_means,
            'bootstrap_samples': bootstrap_samples
        }


# =========================================================
# VISUALIZATION MODULE
# =========================================================

class VisualizationGenerator:
    """
    Generates statistical visualizations.
    """
    
    def __init__(self, output_dir: str = "plots"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
    
    def plot_histogram(self, data: np.ndarray, title: str, xlabel: str, 
                       filename: str, bins: int = 30):
        """
        Create a histogram plot.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.hist(data, bins=bins, edgecolor='black', alpha=0.7, color='steelblue')
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add mean line
        mean_val = np.mean(data)
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, 
                   label=f'Mean: {mean_val:.2f}')
        ax.legend()
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_boxplot(self, data_dict: dict, title: str, filename: str):
        """
        Create a boxplot for multiple metrics.
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Prepare data
        labels = []
        box_data = []
        
        for label, data in data_dict.items():
            labels.append(label.replace('_', ' ').title())
            box_data.append(data)
        
        bp = ax.boxplot(box_data, tick_labels=labels, patch_artist=True)
        
        # Color the boxes
        for patch in bp['boxes']:
            patch.set_facecolor('lightblue')
        
        ax.set_ylabel('Value', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_bootstrap_distribution(self, bootstrap_means: np.ndarray, 
                                     original_mean: float, title: str, filename: str):
        """
        Plot bootstrap distribution of means.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.hist(bootstrap_means, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
        ax.axvline(original_mean, color='red', linestyle='--', linewidth=2, 
                   label=f'Original Mean: {original_mean:.2f}')
        ax.axvline(np.mean(bootstrap_means), color='green', linestyle='-', linewidth=2, 
                   label=f'Bootstrap Mean: {np.mean(bootstrap_means):.2f}')
        
        ax.set_xlabel('Bootstrap Mean', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_confidence_intervals(self, ci_df: pd.DataFrame, title: str, filename: str):
        """
        Plot confidence intervals for multiple metrics.
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        metrics = ci_df.index.tolist()
        means = ci_df['mean'].values
        ci_lower = ci_df['ci_lower'].values
        ci_upper = ci_df['ci_upper'].values
        
        x_pos = np.arange(len(metrics))
        
        ax.errorbar(x_pos, means, yerr=[means - ci_lower, ci_upper - means], 
                    fmt='o', capsize=5, capthick=2, markersize=8, color='steelblue')
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels([m.replace('_', ' ').title() for m in metrics], rotation=45, ha='right')
        ax.set_ylabel('Value', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_time_series(self, metrics_dict: dict, title: str, filename: str):
        """
        Plot time series for multiple metrics.
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for label, (time, data) in metrics_dict.items():
            ax.plot(time, data, label=label, linewidth=2)
        
        ax.set_xlabel('Time (s)', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()


# =========================================================
# HEATMAP ANALYSIS MODULE
# =========================================================

class HeatmapAnalyzer:
    """
    Generates occupancy heatmaps from simulation data.
    """
    
    def __init__(self, world_width: int, world_height: int, output_dir: str = "heatmaps"):
        self.width = world_width
        self.height = world_height
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def accumulate_positions(self, all_position_histories: list) -> np.ndarray:
        """
        Accumulate agent positions across all simulations.
        """
        heatmap = np.zeros((self.height, self.width), dtype=np.float32)
        
        for positions in all_position_histories:
            for x, y in positions:
                if 0 <= x < self.width and 0 <= y < self.height:
                    heatmap[y, x] += 1
        
        return heatmap
    
    def accumulate_deaths(self, all_death_positions: list) -> np.ndarray:
        """
        Accumulate death positions across all simulations.
        """
        heatmap = np.zeros((self.height, self.width), dtype=np.float32)
        
        for positions in all_death_positions:
            for x, y in positions:
                if 0 <= x < self.width and 0 <= y < self.height:
                    heatmap[y, x] += 1
        
        return heatmap
    
    def accumulate_smoke(self, all_smoke_exposure: list) -> np.ndarray:
        """
        Accumulate smoke exposure across all simulations.
        """
        total_smoke = np.zeros((self.height, self.width), dtype=np.float32)
        
        for smoke_matrix in all_smoke_exposure:
            total_smoke += smoke_matrix
        
        return total_smoke
    
    def plot_heatmap(self, heatmap: np.ndarray, title: str, filename: str, 
                     cmap: str = 'YlOrRd'):
        """
        Create and save a heatmap plot.
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        im = ax.imshow(heatmap, cmap=cmap, interpolation='nearest')
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Count', fontsize=12)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('X Position', fontsize=12)
        ax.set_ylabel('Y Position', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
    
    def export_matrix(self, heatmap: np.ndarray, filename: str):
        """
        Export heatmap matrix as CSV.
        """
        pd.DataFrame(heatmap).to_csv(os.path.join(self.output_dir, filename), 
                                      index=False, header=False)


# =========================================================
# MARKDOWN REPORT GENERATOR
# =========================================================

class ReportGenerator:
    """
    Generates a comprehensive markdown report.
    """
    
    def __init__(self, output_file: str = "statistical_report.md"):
        self.output_file = output_file
        self.sections = []
    
    def add_section(self, title: str, content: str):
        """
        Add a section to the report.
        """
        self.sections.append(f"## {title}\n\n{content}\n")
    
    def add_table(self, df: pd.DataFrame, title: str):
        """
        Add a DataFrame as a markdown table.
        """
        # Custom markdown table generator (no tabulate dependency)
        table_lines = []
        
        # Header
        headers = df.index.tolist()
        columns = df.columns.tolist()
        
        # Create header row
        header_row = "| Metric | " + " | ".join(str(col) for col in columns) + " |"
        table_lines.append(header_row)
        
        # Separator
        separator = "|--------|" + "|".join(["--------" for _ in columns]) + "|"
        table_lines.append(separator)
        
        # Data rows
        for idx in df.index:
            row_data = df.loc[idx]
            row_str = "| " + str(idx) + " | " + " | ".join(
                f"{val:.4f}" if isinstance(val, (int, float)) else str(val)
                for val in row_data
            ) + " |"
            table_lines.append(row_str)
        
        table = "\n".join(table_lines)
        self.sections.append(f"### {title}\n\n{table}\n")
    
    def generate_report(self):
        """
        Generate the final markdown report.
        """
        report = f"""# Statistical Analysis of the Evacuation Model

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
        
        for section in self.sections:
            report += section + "\n"
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Report generated: {self.output_file}")


# =========================================================
# MAIN PIPELINE
# =========================================================

def main():
    parser = argparse.ArgumentParser(description="Monte Carlo Analysis for Station Nightclub ABM")
    parser.add_argument("--scenario", type=int, default=1, help="Scenario number (1-6)")
    parser.add_argument("--simulations", type=int, default=100, help="Number of Monte Carlo simulations")
    parser.add_argument("--bootstrap", type=int, default=1000, help="Number of bootstrap samples")
    
    args = parser.parse_args()
    
    # Step 1: Run Monte Carlo simulations
    print("\n" + "="*60)
    print("STEP 1: Running Monte Carlo Simulations")
    print("="*60)
    
    runner = MonteCarloRunner(args.scenario, args.simulations)
    results = runner.run_all_simulations()
    
    if len(results) == 0:
        print("No successful simulations. Exiting.")
        return
    
    # Export raw results
    results_df = pd.DataFrame([{
        'simulation_id': r['simulation_id'],
        'total_evacuated': r['total_evacuated'],
        'total_dead': r['total_dead'],
        'total_injured': r['total_injured'],
        'total_trapped': r['total_trapped'],
        'average_escape_time': r['average_escape_time'],
        'max_density': r['max_density'],
        'average_smoke': r['average_smoke'],
        'window_escape_count': r['window_escape_count'],
        'total_simulation_time': r['total_simulation_time']
    } for r in results])
    
    results_df.to_csv('montecarlo_results.csv', index=False)
    print(f"Results exported to montecarlo_results.csv")
    
    # Step 2: Statistical analysis
    print("\n" + "="*60)
    print("STEP 2: Statistical Analysis")
    print("="*60)
    
    analyzer = StatisticalAnalyzer(results)
    
    # Sample statistics
    sample_stats = analyzer.calculate_sample_statistics()
    sample_stats.to_csv('sample_statistics.csv')
    print("Sample statistics exported to sample_statistics.csv")
    
    # Confidence intervals
    ci_results = analyzer.calculate_confidence_intervals()
    ci_results.to_csv('confidence_intervals.csv')
    print("Confidence intervals exported to confidence_intervals.csv")
    
    # Distribution fitting
    print("\nFitting distributions...")
    dist_results = {}
    for metric in ['total_evacuated', 'total_dead', 'average_escape_time']:
        fits = analyzer.fit_distributions(metric)
        if fits:
            dist_results[metric] = fits
            print(f"  {metric}: Best fit = {fits.get('best_fit', 'N/A')}")
    
    # Export distribution fits
    dist_summary = []
    for metric, fits in dist_results.items():
        for dist_name, fit_data in fits.items():
            if dist_name != 'best_fit':
                dist_summary.append({
                    'metric': metric,
                    'distribution': dist_name,
                    'aic': fit_data['aic'],
                    'bic': fit_data['bic'],
                    'log_likelihood': fit_data['log_likelihood'],
                    'best_fit': fits.get('best_fit', '') == dist_name
                })
    
    if dist_summary:
        dist_df = pd.DataFrame(dist_summary)
        dist_df.to_csv('distribution_fits.csv', index=False)
        print("Distribution fits exported to distribution_fits.csv")
    
    # Bootstrapping
    print("\nPerforming bootstrap analysis...")
    bootstrap_results = {}
    for metric in ['total_evacuated', 'total_dead', 'total_trapped']:
        bs = analyzer.bootstrap_analysis(metric, n_bootstrap=args.bootstrap)
        bootstrap_results[metric] = bs
        print(f"  {metric}: Bootstrap CI = [{bs['bootstrap_ci_lower']:.2f}, {bs['bootstrap_ci_upper']:.2f}]")
    
    # Export bootstrap results
    bs_summary = []
    for metric, bs in bootstrap_results.items():
        bs_summary.append({
            'metric': metric,
            'original_mean': bs['original_mean'],
            'bootstrap_mean': bs['bootstrap_mean'],
            'bootstrap_std': bs['bootstrap_std'],
            'bootstrap_ci_lower': bs['bootstrap_ci_lower'],
            'bootstrap_ci_upper': bs['bootstrap_ci_upper']
        })
    
    bs_df = pd.DataFrame(bs_summary)
    bs_df.to_csv('bootstrap_results.csv', index=False)
    print("Bootstrap results exported to bootstrap_results.csv")
    
    # Step 3: Visualization
    print("\n" + "="*60)
    print("STEP 3: Generating Visualizations")
    print("="*60)
    
    viz = VisualizationGenerator()
    
    # Histograms
    viz.plot_histogram(results_df['total_evacuated'].values, 
                       'Distribution of Evacuated Counts', 
                       'Evacuated Count', 'histogram_evacuated.png')
    print("  Generated histogram_evacuated.png")
    
    viz.plot_histogram(results_df['total_dead'].values, 
                       'Distribution of Death Counts', 
                       'Death Count', 'histogram_deaths.png')
    print("  Generated histogram_deaths.png")
    
    viz.plot_histogram(results_df['average_escape_time'].values, 
                       'Distribution of Average Escape Times', 
                       'Average Escape Time (s)', 'histogram_escape_times.png')
    print("  Generated histogram_escape_times.png")
    
    # Boxplots
    box_data = {
        'Evacuated': results_df['total_evacuated'].values,
        'Dead': results_df['total_dead'].values,
        'Injured': results_df['total_injured'].values,
        'Trapped': results_df['total_trapped'].values
    }
    viz.plot_boxplot(box_data, 'Boxplot of Evacuation Metrics', 'boxplot_metrics.png')
    print("  Generated boxplot_metrics.png")
    
    # Bootstrap distributions
    for metric, bs in bootstrap_results.items():
        viz.plot_bootstrap_distribution(
            bs['bootstrap_means'],
            bs['original_mean'],
            f'Bootstrap Distribution - {metric.replace("_", " ").title()}',
            f'bootstrap_{metric}.png'
        )
        print(f"  Generated bootstrap_{metric}.png")
    
    # Confidence intervals
    viz.plot_confidence_intervals(ci_results, 
                                  '95% Confidence Intervals', 
                                  'confidence_intervals.png')
    print("  Generated confidence_intervals.png")
    
    # Step 4: Heatmap analysis
    print("\n" + "="*60)
    print("STEP 4: Heatmap Analysis")
    print("="*60)
    
    # Get world dimensions from first result
    first_result = results[0]
    if 'smoke_exposure' in first_result:
        height, width = first_result['smoke_exposure'].shape
        
        heatmap_analyzer = HeatmapAnalyzer(width, height)
        
        # Accumulate data
        all_positions = [r['position_history'] for r in results]
        all_deaths = [r['death_positions'] for r in results]
        all_smoke = [r['smoke_exposure'] for r in results]
        
        # Congestion heatmap
        congestion_heatmap = heatmap_analyzer.accumulate_positions(all_positions)
        heatmap_analyzer.plot_heatmap(congestion_heatmap, 
                                      'Congestion Heatmap (Agent Positions)', 
                                      'heatmap_congestion.png')
        heatmap_analyzer.export_matrix(congestion_heatmap, 'congestion_matrix.csv')
        print("  Generated congestion heatmap")
        
        # Death heatmap
        death_heatmap = heatmap_analyzer.accumulate_deaths(all_deaths)
        heatmap_analyzer.plot_heatmap(death_heatmap, 
                                      'Death Heatmap', 
                                      'heatmap_death.png', cmap='Reds')
        heatmap_analyzer.export_matrix(death_heatmap, 'death_matrix.csv')
        print("  Generated death heatmap")
        
        # Smoke exposure heatmap
        smoke_heatmap = heatmap_analyzer.accumulate_smoke(all_smoke)
        heatmap_analyzer.plot_heatmap(smoke_heatmap, 
                                      'Smoke Exposure Heatmap', 
                                      'heatmap_smoke.png', cmap='Greys')
        heatmap_analyzer.export_matrix(smoke_heatmap, 'smoke_matrix.csv')
        print("  Generated smoke exposure heatmap")
    
    # Step 5: Generate report
    print("\n" + "="*60)
    print("STEP 5: Generating Markdown Report")
    print("="*60)
    
    report = ReportGenerator()
    
    report.add_section("Monte Carlo Methodology", 
                       f"This analysis performed {args.simulations} Monte Carlo simulations "
                       f"of Scenario {args.scenario} ({runner.cfg['name']}). "
                       f"Each simulation used a different random seed to ensure independence. "
                       f"The simulation ran for {runner.cfg['simulation_steps']} timesteps (seconds).")
    
    report.add_section("Simulation Configuration",
                       f"- Scenario: {args.scenario}\n"
                       f"- Name: {runner.cfg['name']}\n"
                       f"- Number of agents: {runner.cfg['n_agents']}\n"
                       f"- Simulation steps: {runner.cfg['simulation_steps']}\n"
                       f"- Follow group probability: {runner.cfg['follow_group_prob']}\n"
                       f"- Reaction time multiplier: {runner.cfg['reaction_time_multiplier']}")
    
    report.add_table(sample_stats, "Sample Statistics")
    report.add_table(ci_results, "95% Confidence Intervals")
    
    if dist_summary:
        report.add_section("Distribution Fitting", 
                           "Distributions were fitted using Maximum Likelihood Estimation (MLE). "
                           "The best-fitting distribution was selected based on Akaike Information Criterion (AIC).")
        report.add_table(dist_df, "Distribution Fit Results")
    
    report.add_table(bs_df, "Bootstrap Analysis Results")
    
    report.add_section("Conclusions",
                       f"The Monte Carlo analysis provides robust statistical estimates of evacuation outcomes. "
                       f"Based on {len(results)} successful simulations, the model predicts "
                       f"an average of {sample_stats.loc['total_evacuated', 'mean']:.1f} evacuated persons "
                       f"(95% CI: [{ci_results.loc['total_evacuated', 'ci_lower']:.1f}, "
                       f"{ci_results.loc['total_evacuated', 'ci_upper']:.1f}]) and "
                       f"an average of {sample_stats.loc['total_dead', 'mean']:.1f} fatalities "
                       f"(95% CI: [{ci_results.loc['total_dead', 'ci_lower']:.1f}, "
                       f"{ci_results.loc['total_dead', 'ci_upper']:.1f}]). "
                       f"The bootstrap analysis confirms the stability of these estimates.")
    
    report.generate_report()
    
    print("\n" + "="*60)
    print("MONTE CARLO ANALYSIS COMPLETE")
    print("="*60)
    print(f"Successful simulations: {len(results)}/{args.simulations}")
    print(f"Results exported to: montecarlo_results.csv")
    print(f"Plots saved to: plots/")
    print(f"Heatmaps saved to: heatmaps/")
    print(f"Report generated: statistical_report.md")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
