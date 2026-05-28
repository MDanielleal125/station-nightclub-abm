"""
Run All Scenarios - Batch Execution Script

This script automatically executes both Monte Carlo analysis and
Convergence analysis for all 6 scenarios, organizing results in
scenario-specific directories.

Usage:
    python run_all_scenarios.py
    python run_all_scenarios.py --scenarios 1,2,3
    python run_all_scenarios.py --skip-convergence
    python run_all_scenarios.py --skip-montecarlo
"""

import argparse
import os
import subprocess
import shutil
from datetime import datetime

# Configuration
ALL_SCENARIOS = [1, 2, 3, 4, 5, 6]


def run_command(cmd: str, description: str):
    """
    Execute a command and print status.
    """
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}\n")
    
    result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
    
    if result.returncode == 0:
        print(f"✓ {description} - SUCCESS")
    else:
        print(f"✗ {description} - FAILED (exit code: {result.returncode})")
    
    return result.returncode == 0


def organize_scenario_results(scenario_num: int):
    """
    Organize results for a specific scenario into a dedicated directory.
    """
    scenario_dir = f"scenario_{scenario_num}"
    os.makedirs(scenario_dir, exist_ok=True)
    
    # Files to move
    files_to_move = [
        'montecarlo_results.csv',
        'sample_statistics.csv',
        'confidence_intervals.csv',
        'distribution_fits.csv',
        'bootstrap_results.csv',
        'convergence_data.csv',
        'statistical_report.md'
    ]
    
    # Directories to move/copy
    dirs_to_copy = ['plots', 'heatmaps']
    
    # Move CSV files
    for filename in files_to_move:
        if os.path.exists(filename):
            dest = os.path.join(scenario_dir, filename)
            # If file exists, rename with scenario number
            if os.path.exists(dest):
                base, ext = os.path.splitext(filename)
                dest = os.path.join(scenario_dir, f"{base}_s{scenario_num}{ext}")
            shutil.move(filename, dest)
            print(f"  Moved {filename} -> {dest}")
    
    # Copy directories
    for dirname in dirs_to_copy:
        if os.path.exists(dirname):
            dest = os.path.join(scenario_dir, dirname)
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(dirname, dest)
            print(f"  Copied {dirname}/ -> {dest}/")
            shutil.rmtree(dirname)


def run_scenario_analysis(scenario_num: int, run_convergence: bool, run_montecarlo: bool,
                          pilot_sims: int, mc_sims: int, bootstrap_sims: int):
    """
    Run both analyses for a single scenario.
    """
    print(f"\n{'#'*60}")
    print(f"# SCENARIO {scenario_num}")
    print(f"{'#'*60}")
    
    # Change to scenario-specific directory for outputs
    scenario_dir = f"scenario_{scenario_num}"
    os.makedirs(scenario_dir, exist_ok=True)
    
    # Run convergence analysis
    if run_convergence:
        cmd = f"python simulation_convergence.py --scenario {scenario_num} --pilot {pilot_sims}"
        success = run_command(cmd, f"Convergence Analysis - Scenario {scenario_num}")
        if not success:
            print(f"WARNING: Convergence analysis failed for scenario {scenario_num}")
    
    # Run Monte Carlo analysis
    if run_montecarlo:
        cmd = f"python montecarlo_analysis.py --scenario {scenario_num} --simulations {mc_sims} --bootstrap {bootstrap_sims}"
        success = run_command(cmd, f"Monte Carlo Analysis - Scenario {scenario_num}")
        if not success:
            print(f"WARNING: Monte Carlo analysis failed for scenario {scenario_num}")
    
    # Organize results
    print(f"\nOrganizing results for scenario {scenario_num}...")
    organize_scenario_results(scenario_num)
    
    print(f"✓ Scenario {scenario_num} complete")


def generate_summary_report(scenarios: list):
    """
    Generate a summary report comparing all scenarios.
    """
    report_path = "all_scenarios_summary.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# All Scenarios Analysis Summary\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## Scenarios Analyzed\n\n")
        
        scenario_names = {
            1: "Base",
            2: "Alta Congestión",
            3: "Más Humo",
            4: "Salidas Bloqueadas",
            5: "Comportamiento Grupal Fuerte",
            6: "Reacción Tardía"
        }
        
        for scen in scenarios:
            f.write(f"- **Scenario {scen}**: {scenario_names.get(scen, 'Unknown')}\n")
        
        f.write(f"\n## Results Organization\n\n")
        f.write(f"Each scenario has its own directory:\n\n")
        for scen in scenarios:
            f.write(f"- `scenario_{scen}/` - Results for Scenario {scen}\n")
        
        f.write(f"\n## Contents per Scenario\n\n")
        f.write(f"Each scenario directory contains:\n\n")
        f.write(f"- CSV files with statistical results\n")
        f.write(f"- `plots/` - Visualization PNG files\n")
        f.write(f"- `heatmaps/` - Heatmap PNG and CSV files\n")
        f.write(f"- `statistical_report.md` - Detailed markdown report\n")
        
        f.write(f"\n## Next Steps\n\n")
        f.write(f"Review individual scenario reports in each `scenario_N/` directory.\n")
        f.write(f"Compare results across scenarios to analyze the impact of different factors.\n")
    
    print(f"\n✓ Summary report generated: {report_path}")


def main():
    parser = argparse.ArgumentParser(description="Run analysis for all scenarios")
    parser.add_argument("--scenarios", type=str, default="1,2,3,4,5,6",
                       help="Comma-separated scenario numbers (e.g., 1,2,3)")
    parser.add_argument("--skip-convergence", action="store_true",
                       help="Skip convergence analysis")
    parser.add_argument("--skip-montecarlo", action="store_true",
                       help="Skip Monte Carlo analysis")
    parser.add_argument("--pilot", type=int, default=10,
                       help="Number of pilot simulations for convergence")
    parser.add_argument("--simulations", type=int, default=50,
                       help="Number of Monte Carlo simulations per scenario")
    parser.add_argument("--bootstrap", type=int, default=1000,
                       help="Number of bootstrap samples for Monte Carlo analysis")
    
    args = parser.parse_args()
    
    # Parse scenarios
    scenarios = [int(x.strip()) for x in args.scenarios.split(',')]
    
    print(f"\n{'='*60}")
    print("BATCH ANALYSIS - ALL SCENARIOS")
    print(f"{'='*60}")
    print(f"Scenarios to analyze: {scenarios}")
    print(f"Run convergence: {not args.skip_convergence}")
    print(f"Run Monte Carlo: {not args.skip_montecarlo}")
    print(f"Pilot simulations: {args.pilot}")
    print(f"Monte Carlo simulations: {args.simulations}")
    print(f"Bootstrap samples: {args.bootstrap}")
    print(f"{'='*60}\n")
    
    if args.skip_convergence and args.skip_montecarlo:
        print("ERROR: Both analyses skipped. Nothing to do.")
        return
    
    # Run analysis for each scenario
    start_time = datetime.now()
    
    for scenario_num in scenarios:
        run_scenario_analysis(
            scenario_num=scenario_num,
            run_convergence=not args.skip_convergence,
            run_montecarlo=not args.skip_montecarlo,
            pilot_sims=args.pilot,
            mc_sims=args.simulations,
            bootstrap_sims=args.bootstrap
        )
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Generate summary report
    generate_summary_report(scenarios)
    
    print(f"\n{'='*60}")
    print("BATCH ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"Total time: {duration/60:.1f} minutes")
    print(f"Scenarios processed: {len(scenarios)}")
    print(f"\nResults organized in:")
    for scen in scenarios:
        print(f"  - scenario_{scen}/")
    print(f"\nSummary report: all_scenarios_summary.md")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
