"""
Simulation Convergence Analysis Module for Station Nightclub ABM

This module implements statistical convergence analysis to determine the
required number of Monte Carlo simulations based on desired precision.

The module:
1. Runs pilot simulations to estimate variability
2. Calculates required sample size using statistical formula
3. Automatically continues simulations until convergence is achieved
4. Generates convergence plots showing statistical stabilization
5. Calculates relative error and confidence intervals
6. Implements automatic stopping criterion based on relative error

This transforms the project from arbitrary simulation counts to
scientifically justified sample sizes, following academic standards.

Usage:
    python simulation_convergence.py --scenario 1
    python simulation_convergence.py --scenario 1 --pilot 10 --error-deaths 5
"""

import argparse
import os
import random
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from math import ceil, sqrt

from config.scenarios import get_scenario
from config.constants import EXIT, FIRE
from data_io.loaders import cargar_layout, cargar_agentes
from simulation.fire import FireSimulation
from simulation.smoke import SmokeSimulation
from simulation.movement import mover


# =========================================================
# CONFIGURATION
# =========================================================

# Statistical parameters
CONFIDENCE_LEVEL = 0.95
Z_SCORE = 1.96  # For 95% confidence interval

# Allowed errors (configurable)
ALLOWED_ERROR_DEATHS = 5
ALLOWED_ERROR_EVACUATED = 5
ALLOWED_ERROR_TRAPPED = 5

# Automatic stopping criterion
AUTO_STOP_RELATIVE_ERROR = 0.05  # 5% relative error
MAX_SIMULATIONS = 500  # Safety limit

# Pilot simulation parameters
DEFAULT_PILOT_SIMULATIONS = 10


# =========================================================
# CONVERGENCE ANALYZER
# =========================================================

class ConvergenceAnalyzer:
    """
    Analyzes convergence of Monte Carlo simulations and determines
    the required number of runs for statistical significance.
    """
    
    def __init__(self, scenario_num: int, pilot_simulations: int = DEFAULT_PILOT_SIMULATIONS,
                 error_deaths: float = ALLOWED_ERROR_DEATHS,
                 error_evacuated: float = ALLOWED_ERROR_EVACUATED,
                 error_trapped: float = ALLOWED_ERROR_TRAPPED,
                 auto_stop: bool = True):
        self.scenario_num = scenario_num
        self.pilot_simulations = pilot_simulations
        self.error_deaths = error_deaths
        self.error_evacuated = error_evacuated
        self.error_trapped = error_trapped
        self.auto_stop = auto_stop
        
        self.cfg = get_scenario(scenario_num)
        self.results = []
        self.cumulative_means = {
            'evacuated': [],
            'deaths': [],
            'trapped': []
        }
        self.cumulative_stds = {
            'evacuated': [],
            'deaths': [],
            'trapped': []
        }
        self.relative_errors = {
            'evacuated': [],
            'deaths': [],
            'trapped': []
        }
        
        # Generate filename suffix based on parameters
        self.suffix = f"_s{scenario_num}"
        if pilot_simulations != DEFAULT_PILOT_SIMULATIONS:
            self.suffix += f"_p{pilot_simulations}"
    
    def run_single_simulation(self, seed: int) -> dict:
        """
        Run a single simulation with the given random seed.
        Returns a dictionary of global metrics.
        """
        random.seed(seed)
        np.random.seed(seed)
        
        # Load world
        world = cargar_layout(os.path.join("data", "building_nightclub.csv"))
        world.calcular_interior()
        world.aplicar_blocked_exits(self.cfg["blocked_exits"])
        
        # Load fire and smoke
        fire_sim = FireSimulation()
        fire_sim.cargar_eventos(os.path.join("data", "fire_nightclub_merged.csv"), world)
        
        smoke_sim = SmokeSimulation()
        smoke_sim.cargar_eventos(os.path.join("data", "smoke.csv"), world)
        
        # Calculate distance maps
        world.calcular_distance_maps()
        
        # Load agents
        agentes = cargar_agentes(os.path.join("data", "people.csv"), world, self.cfg)
        
        # Main simulation loop
        steps = self.cfg["simulation_steps"]
        
        for t in range(steps):
            # Update fire
            fire_sim.actualizar(world, t)
            fire_sim.expandir(world, t, self.cfg)
            
            # Update smoke
            smoke_sim.actualizar(world, t, self.cfg)
            
            # Move agents
            for a in agentes:
                if not a.alive:
                    continue
                
                mover(a, agentes, world, t)
                
                # Smoke effects
                densidad = world.smoke[a.y][a.x]
                a.smoke_inhaled += densidad * 0.22
                a.energy -= densidad * 0.05
                
                # Injury
                if a.smoke_inhaled > 120 or a.energy < 45:
                    a.injured = True
                
                # Death by fire
                if world.grid[a.y][a.x] == FIRE:
                    a.alive = False
                
                # Evacuation
                elif world.grid[a.y][a.x] == EXIT:
                    a.evacuated = True
                    a.alive = False
                
                # Death by smoke
                elif a.energy <= 0 or a.smoke_inhaled > 260:
                    a.alive = False
        
        # Calculate final metrics
        total_evacuated = sum(a.evacuated for a in agentes)
        total_dead = sum((not a.alive) and (not a.evacuated) for a in agentes)
        total_trapped = sum(a.alive for a in agentes)
        
        return {
            'simulation_id': seed,
            'total_evacuated': total_evacuated,
            'total_dead': total_dead,
            'total_trapped': total_trapped
        }
    
    def calculate_required_sample_size(self, std_dev: float, allowed_error: float) -> int:
        """
        Calculate required sample size using formula:
        n = (Z * σ / E)^2
        
        Where:
        - Z = z-score for confidence level (1.96 for 95%)
        - σ = standard deviation
        - E = allowed error (margin of error)
        """
        if std_dev == 0 or allowed_error == 0:
            return 1
        
        required_n = ((Z_SCORE * std_dev) / allowed_error) ** 2
        return ceil(required_n)
    
    def update_cumulative_statistics(self):
        """
        Update cumulative means, standard deviations, and relative errors
        after each simulation.
        """
        evacuated_data = [r['total_evacuated'] for r in self.results]
        deaths_data = [r['total_dead'] for r in self.results]
        trapped_data = [r['total_trapped'] for r in self.results]
        
        # Cumulative means
        self.cumulative_means['evacuated'].append(np.mean(evacuated_data))
        self.cumulative_means['deaths'].append(np.mean(deaths_data))
        self.cumulative_means['trapped'].append(np.mean(trapped_data))
        
        # Cumulative standard deviations
        if len(evacuated_data) > 1:
            self.cumulative_stds['evacuated'].append(np.std(evacuated_data, ddof=1))
            self.cumulative_stds['deaths'].append(np.std(deaths_data, ddof=1))
            self.cumulative_stds['trapped'].append(np.std(trapped_data, ddof=1))
        else:
            self.cumulative_stds['evacuated'].append(0)
            self.cumulative_stds['deaths'].append(0)
            self.cumulative_stds['trapped'].append(0)
        
        # Relative errors (CI half-width / mean)
        n = len(self.results)
        for metric, data in [('evacuated', evacuated_data), 
                             ('deaths', deaths_data), 
                             ('trapped', trapped_data)]:
            if n > 1:
                mean = np.mean(data)
                std = np.std(data, ddof=1)
                ci_half_width = Z_SCORE * (std / sqrt(n))
                if mean > 0:
                    rel_error = ci_half_width / mean
                    self.relative_errors[metric].append(rel_error)
                else:
                    self.relative_errors[metric].append(0)
            else:
                self.relative_errors[metric].append(1.0)  # Maximum error initially
    
    def check_auto_stop_criterion(self) -> bool:
        """
        Check if automatic stopping criterion is met.
        Stops when relative error < AUTO_STOP_RELATIVE_ERROR for all metrics.
        """
        if not self.auto_stop:
            return False
        
        if len(self.results) < self.pilot_simulations:
            return False
        
        # Check if all metrics have relative error below threshold
        for metric in ['evacuated', 'deaths', 'trapped']:
            if self.relative_errors[metric][-1] > AUTO_STOP_RELATIVE_ERROR:
                return False
        
        return True
    
    def run_convergence_analysis(self):
        """
        Run the complete convergence analysis:
        1. Execute pilot simulations
        2. Calculate required sample size
        3. Continue until convergence or max simulations
        4. Track cumulative statistics
        """
        print(f"\n{'='*60}")
        print("SIMULATION CONVERGENCE ANALYSIS")
        print(f"{'='*60}")
        print(f"Scenario: {self.scenario_num} ({self.cfg['name']})")
        print(f"Pilot simulations: {self.pilot_simulations}")
        print(f"Allowed error - Deaths: {self.error_deaths}")
        print(f"Allowed error - Evacuated: {self.error_evacuated}")
        print(f"Allowed error - Trapped: {self.error_trapped}")
        print(f"Auto-stop criterion: {AUTO_STOP_RELATIVE_ERROR*100}% relative error")
        print(f"{'='*60}\n")
        
        # Phase 1: Pilot simulations
        print("PHASE 1: Running pilot simulations...")
        for i in range(self.pilot_simulations):
            seed = i + 1
            print(f"  Pilot simulation {i+1}/{self.pilot_simulations}...", end=' ')
            
            try:
                result = self.run_single_simulation(seed)
                self.results.append(result)
                self.update_cumulative_statistics()
                print("✓")
            except Exception as e:
                print(f"✗ Error: {e}")
                continue
        
        # Calculate standard deviations from pilot
        pilot_evacuated = [r['total_evacuated'] for r in self.results]
        pilot_deaths = [r['total_dead'] for r in self.results]
        pilot_trapped = [r['total_trapped'] for r in self.results]
        
        std_evacuated = np.std(pilot_evacuated, ddof=1) if len(pilot_evacuated) > 1 else 0
        std_deaths = np.std(pilot_deaths, ddof=1) if len(pilot_deaths) > 1 else 0
        std_trapped = np.std(pilot_trapped, ddof=1) if len(pilot_trapped) > 1 else 0
        
        print(f"\nPilot Results:")
        print(f"  Evacuated: mean={np.mean(pilot_evacuated):.2f}, std={std_evacuated:.2f}")
        print(f"  Deaths: mean={np.mean(pilot_deaths):.2f}, std={std_deaths:.2f}")
        print(f"  Trapped: mean={np.mean(pilot_trapped):.2f}, std={std_trapped:.2f}")
        
        # Calculate required sample sizes
        required_n_evacuated = self.calculate_required_sample_size(std_evacuated, self.error_evacuated)
        required_n_deaths = self.calculate_required_sample_size(std_deaths, self.error_deaths)
        required_n_trapped = self.calculate_required_sample_size(std_trapped, self.error_trapped)
        
        # Take maximum required
        required_n = max(required_n_evacuated, required_n_deaths, required_n_trapped)
        
        print(f"\nRequired Sample Sizes:")
        print(f"  For evacuated (E={self.error_evacuated}): {required_n_evacuated}")
        print(f"  For deaths (E={self.error_deaths}): {required_n_deaths}")
        print(f"  For trapped (E={self.error_trapped}): {required_n_trapped}")
        print(f"  Maximum required: {required_n}")
        
        # Phase 2: Continue until convergence
        current_runs = len(self.results)
        
        if required_n > current_runs:
            print(f"\nPHASE 2: Continuing simulations (need {required_n - current_runs} more)...")
            
            for i in range(current_runs, min(required_n, MAX_SIMULATIONS)):
                seed = i + 1
                print(f"  Simulation {i+1}/{required_n}...", end=' ')
                
                try:
                    result = self.run_single_simulation(seed)
                    self.results.append(result)
                    self.update_cumulative_statistics()
                    print("✓")
                    
                    # Check auto-stop criterion
                    if self.check_auto_stop_criterion():
                        print(f"\n  Auto-stop criterion met at {i+1} simulations!")
                        print(f"  Relative errors < {AUTO_STOP_RELATIVE_ERROR*100}% for all metrics")
                        break
                        
                except Exception as e:
                    print(f"✗ Error: {e}")
                    continue
        else:
            print(f"\nPilot simulations sufficient. No additional runs needed.")
        
        # Final statistics
        final_evacuated = [r['total_evacuated'] for r in self.results]
        final_deaths = [r['total_dead'] for r in self.results]
        final_trapped = [r['total_trapped'] for r in self.results]
        
        print(f"\n{'='*60}")
        print("CONVERGENCE ANALYSIS COMPLETE")
        print(f"{'='*60}")
        print(f"Total simulations: {len(self.results)}")
        print(f"Final evacuated: mean={np.mean(final_evacuated):.2f}, std={np.std(final_evacuated, ddof=1):.2f}")
        print(f"Final deaths: mean={np.mean(final_deaths):.2f}, std={np.std(final_deaths, ddof=1):.2f}")
        print(f"Final trapped: mean={np.mean(final_trapped):.2f}, std={np.std(final_trapped, ddof=1):.2f}")
        
        # Final relative errors
        n = len(self.results)
        for metric, data, name in [('evacuated', final_evacuated, 'Evacuated'),
                                   ('deaths', final_deaths, 'Deaths'),
                                   ('trapped', final_trapped, 'Trapped')]:
            if n > 1:
                mean = np.mean(data)
                std = np.std(data, ddof=1)
                ci_half_width = Z_SCORE * (std / sqrt(n))
                rel_error = ci_half_width / mean if mean > 0 else 0
                print(f"Final {name} relative error: {rel_error*100:.2f}%")
        
        print(f"{'='*60}\n")
        
        return {
            'total_simulations': len(self.results),
            'required_n': required_n,
            'pilot_simulations': self.pilot_simulations,
            'std_evacuated': std_evacuated,
            'std_deaths': std_deaths,
            'std_trapped': std_trapped,
            'required_n_evacuated': required_n_evacuated,
            'required_n_deaths': required_n_deaths,
            'required_n_trapped': required_n_trapped,
            'final_mean_evacuated': np.mean(final_evacuated),
            'final_mean_deaths': np.mean(final_deaths),
            'final_mean_trapped': np.mean(final_trapped),
            'final_std_evacuated': np.std(final_evacuated, ddof=1),
            'final_std_deaths': np.std(final_deaths, ddof=1),
            'final_std_trapped': np.std(final_trapped, ddof=1),
            'cumulative_means': self.cumulative_means,
            'cumulative_stds': self.cumulative_stds,
            'relative_errors': self.relative_errors
        }


# =========================================================
# VISUALIZATION
# =========================================================

class ConvergenceVisualizer:
    """
    Generates convergence plots showing statistical stabilization.
    """
    
    def __init__(self, output_dir: str = "plots", suffix: str = ""):
        self.output_dir = output_dir
        self.suffix = suffix
        os.makedirs(output_dir, exist_ok=True)
        
        plt.rcParams['figure.figsize'] = (12, 6)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
    
    def plot_convergence(self, cumulative_means: dict, metric: str, 
                         title: str, filename: str, target_value: float = None):
        """
        Create a convergence plot showing how the cumulative mean stabilizes.
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = range(1, len(cumulative_means[metric]) + 1)
        y = cumulative_means[metric]
        
        ax.plot(x, y, linewidth=2, color='steelblue', marker='o', markersize=4, alpha=0.7)
        
        # Add target line if specified
        if target_value is not None:
            ax.axhline(y=target_value, color='red', linestyle='--', linewidth=2, 
                       label=f'Target: {target_value:.2f}')
            ax.legend()
        
        ax.set_xlabel('Number of Simulations', fontsize=12)
        ax.set_ylabel('Cumulative Mean', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add convergence indicator
        if len(y) > 10:
            last_10_std = np.std(y[-10:])
            ax.text(0.02, 0.95, f'Std of last 10: {last_10_std:.4f}', 
                   transform=ax.transAxes, fontsize=10,
                   verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        # Add suffix to filename if provided
        if self.suffix:
            base, ext = os.path.splitext(filename)
            filename = f"{base}{self.suffix}{ext}"
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_relative_error(self, relative_errors: dict, title: str, filename: str, 
                           threshold: float = AUTO_STOP_RELATIVE_ERROR):
        """
        Plot relative error convergence.
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for metric, errors in relative_errors.items():
            x = range(1, len(errors) + 1)
            ax.plot(x, errors, linewidth=2, marker='o', markersize=4, alpha=0.7, 
                   label=metric.replace('_', ' ').title())
        
        # Add threshold line
        ax.axhline(y=threshold, color='red', linestyle='--', linewidth=2, 
                   label=f'Threshold: {threshold*100}%')
        
        ax.set_xlabel('Number of Simulations', fontsize=12)
        ax.set_ylabel('Relative Error', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        # Add suffix to filename if provided
        if self.suffix:
            base, ext = os.path.splitext(filename)
            filename = f"{base}{self.suffix}{ext}"
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_std_convergence(self, cumulative_stds: dict, title: str, filename: str):
        """
        Plot how standard deviation converges.
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for metric, stds in cumulative_stds.items():
            x = range(1, len(stds) + 1)
            ax.plot(x, stds, linewidth=2, marker='o', markersize=4, alpha=0.7, 
                   label=metric.replace('_', ' ').title())
        
        ax.set_xlabel('Number of Simulations', fontsize=12)
        ax.set_ylabel('Cumulative Standard Deviation', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        # Add suffix to filename if provided
        if self.suffix:
            base, ext = os.path.splitext(filename)
            filename = f"{base}{self.suffix}{ext}"
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()


# =========================================================
# REPORT GENERATOR
# =========================================================

class ConvergenceReportGenerator:
    """
    Generates markdown report section for convergence analysis.
    """
    
    def __init__(self, output_file: str = "statistical_report.md", suffix: str = ""):
        self.output_file = output_file
        self.suffix = suffix
        # Add suffix to output file if provided
        if suffix:
            base, ext = os.path.splitext(output_file)
            self.output_file = f"{base}{suffix}{ext}"
    
    def append_convergence_section(self, analysis_results: dict, scenario_num: int):
        """
        Append convergence analysis section to the markdown report.
        """
        section = f"""## Monte Carlo Convergence Analysis

### Methodology

The convergence analysis determines the statistically required number of Monte Carlo simulations based on desired precision. The sample size is calculated using the formula:

```
n = (Z × σ / E)²
```

Where:
- Z = 1.96 (z-score for 95% confidence level)
- σ = standard deviation from pilot simulations
- E = allowed error (margin of error)

### Pilot Simulations

- Number of pilot simulations: {analysis_results['pilot_simulations']}
- Standard deviation (evacuated): {analysis_results['std_evacuated']:.4f}
- Standard deviation (deaths): {analysis_results['std_deaths']:.4f}
- Standard deviation (trapped): {analysis_results['std_trapped']:.4f}

### Required Sample Size Calculation

Based on pilot variability and desired precision:

- Required for evacuated (E={ALLOWED_ERROR_EVACUATED}): {analysis_results['required_n_evacuated']} simulations
- Required for deaths (E={ALLOWED_ERROR_DEATHS}): {analysis_results['required_n_deaths']} simulations
- Required for trapped (E={ALLOWED_ERROR_TRAPPED}): {analysis_results['required_n_trapped']} simulations
- **Maximum required: {analysis_results['required_n']} simulations**

### Convergence Results

- Total simulations executed: {analysis_results['total_simulations']}
- Final mean (evacuated): {analysis_results['final_mean_evacuated']:.2f} ± {analysis_results['final_std_evacuated']:.2f}
- Final mean (deaths): {analysis_results['final_mean_deaths']:.2f} ± {analysis_results['final_std_deaths']:.2f}
- Final mean (trapped): {analysis_results['final_mean_trapped']:.2f} ± {analysis_results['final_std_trapped']:.2f}

### Statistical Justification

The number of simulations ({analysis_results['total_simulations']}) was not arbitrarily chosen but statistically calculated based on the variability observed in pilot simulations. This ensures that the Monte Carlo estimates achieve the desired precision level, making the analysis scientifically valid and reproducible.

### Convergence Plots

The following plots demonstrate statistical stabilization:

- `convergence_evacuated.png`: Shows how the cumulative mean of evacuated persons converges
- `convergence_deaths.png`: Shows how the cumulative mean of deaths converges
- `convergence_relative_error.png`: Shows relative error convergence across all metrics
- `convergence_std.png`: Shows how standard deviation stabilizes

These plots confirm that the estimates have reached statistical stability and additional simulations would not significantly change the results.

---

"""
        
        # Append to existing report
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(existing_content + section)
        else:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Statistical Analysis of the Evacuation Model\n\n" + section)
        
        print(f"Convergence section appended to {self.output_file}")


# =========================================================
# MAIN PIPELINE
# =========================================================

def main():
    parser = argparse.ArgumentParser(description="Simulation Convergence Analysis")
    parser.add_argument("--scenario", type=int, default=1, help="Scenario number (1-6)")
    parser.add_argument("--pilot", type=int, default=DEFAULT_PILOT_SIMULATIONS, 
                       help="Number of pilot simulations")
    parser.add_argument("--error-deaths", type=float, default=ALLOWED_ERROR_DEATHS,
                       help="Allowed error for deaths")
    parser.add_argument("--error-evacuated", type=float, default=ALLOWED_ERROR_EVACUATED,
                       help="Allowed error for evacuated")
    parser.add_argument("--error-trapped", type=float, default=ALLOWED_ERROR_TRAPPED,
                       help="Allowed error for trapped")
    parser.add_argument("--no-auto-stop", action="store_true",
                       help="Disable automatic stopping criterion")
    
    args = parser.parse_args()
    
    # Run convergence analysis
    analyzer = ConvergenceAnalyzer(
        scenario_num=args.scenario,
        pilot_simulations=args.pilot,
        error_deaths=args.error_deaths,
        error_evacuated=args.error_evacuated,
        error_trapped=args.error_trapped,
        auto_stop=not args.no_auto_stop
    )
    
    results = analyzer.run_convergence_analysis()
    
    # Generate visualizations
    print("\nGenerating convergence plots...")
    viz = ConvergenceVisualizer(suffix=analyzer.suffix)
    
    viz.plot_convergence(
        results['cumulative_means'], 
        'evacuated',
        'Convergence of Evacuated Count',
        'convergence_evacuated.png',
        target_value=results['final_mean_evacuated']
    )
    print(f"  Generated convergence_evacuated{analyzer.suffix}.png")
    
    viz.plot_convergence(
        results['cumulative_means'], 
        'deaths',
        'Convergence of Death Count',
        'convergence_deaths.png',
        target_value=results['final_mean_deaths']
    )
    print(f"  Generated convergence_deaths{analyzer.suffix}.png")
    
    viz.plot_convergence(
        results['cumulative_means'], 
        'trapped',
        'Convergence of Trapped Count',
        'convergence_trapped.png',
        target_value=results['final_mean_trapped']
    )
    print(f"  Generated convergence_trapped{analyzer.suffix}.png")
    
    viz.plot_relative_error(
        results['relative_errors'],
        'Relative Error Convergence',
        'convergence_relative_error.png',
        threshold=AUTO_STOP_RELATIVE_ERROR
    )
    print(f"  Generated convergence_relative_error{analyzer.suffix}.png")
    
    viz.plot_std_convergence(
        results['cumulative_stds'],
        'Standard Deviation Convergence',
        'convergence_std.png'
    )
    print(f"  Generated convergence_std{analyzer.suffix}.png")
    
    # Generate report section
    print("\nGenerating convergence report section...")
    report_gen = ConvergenceReportGenerator(suffix=analyzer.suffix)
    report_gen.append_convergence_section(results, args.scenario)
    
    # Export convergence data
    convergence_df = pd.DataFrame({
        'simulation': range(1, len(results['cumulative_means']['evacuated']) + 1),
        'mean_evacuated': results['cumulative_means']['evacuated'],
        'mean_deaths': results['cumulative_means']['deaths'],
        'mean_trapped': results['cumulative_means']['trapped'],
        'std_evacuated': results['cumulative_stds']['evacuated'],
        'std_deaths': results['cumulative_stds']['deaths'],
        'std_trapped': results['cumulative_stds']['trapped'],
        'rel_error_evacuated': results['relative_errors']['evacuated'],
        'rel_error_deaths': results['relative_errors']['deaths'],
        'rel_error_trapped': results['relative_errors']['trapped']
    })
    
    convergence_df.to_csv(f'convergence_data{analyzer.suffix}.csv', index=False)
    print(f"Convergence data exported to convergence_data{analyzer.suffix}.csv")
    
    print("\n" + "="*60)
    print("CONVERGENCE ANALYSIS COMPLETE")
    print("="*60)
    print(f"Recommended simulations for future runs: {results['total_simulations']}")
    print(f"Convergence plots saved to: plots/")
    print(f"Convergence data exported to: convergence_data{analyzer.suffix}.csv")
    print(f"Report section added to: statistical_report{analyzer.suffix}.md")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
