# Statistical Analysis of the Evacuation Model

Generated: 2026-05-28 01:44:12

---

## Monte Carlo Methodology

This analysis performed 2 Monte Carlo simulations of Scenario 1 (Escenario 1 — Base). Each simulation used a different random seed to ensure independence. The simulation ran for 300 timesteps (seconds).

## Simulation Configuration

- Scenario: 1
- Name: Escenario 1 — Base
- Number of agents: 465
- Simulation steps: 300
- Follow group probability: 0.65
- Reaction time multiplier: 1.0

### Sample Statistics

| Metric | mean | variance | std_dev | min | max | median | q25 | q75 |
|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| total_evacuated | 186.5000 | 0.5000 | 0.7071 | 186.0000 | 187.0000 | 186.5000 | 186.2500 | 186.7500 |
| total_dead | 101.5000 | 12.5000 | 3.5355 | 99.0000 | 104.0000 | 101.5000 | 100.2500 | 102.7500 |
| total_injured | 126.5000 | 144.5000 | 12.0208 | 118.0000 | 135.0000 | 126.5000 | 122.2500 | 130.7500 |
| total_trapped | 177.0000 | 8.0000 | 2.8284 | 175.0000 | 179.0000 | 177.0000 | 176.0000 | 178.0000 |
| average_escape_time | 167.4300 | 11.3976 | 3.3760 | 165.0428 | 169.8172 | 167.4300 | 166.2364 | 168.6236 |
| max_density | 4.1312 | 0.0000 | 0.0000 | 4.1312 | 4.1312 | 4.1312 | 4.1312 | 4.1312 |
| average_smoke | 917.9867 | 66.2648 | 8.1403 | 912.2306 | 923.7428 | 917.9867 | 915.1087 | 920.8648 |

### 95% Confidence Intervals

| Metric | mean | std | margin_of_error | ci_lower | ci_upper | confidence_level |
|--------|--------|--------|--------|--------|--------|--------|
| total_evacuated | 186.5000 | 0.7071 | 0.9800 | 185.5200 | 187.4800 | 0.9500 |
| total_dead | 101.5000 | 3.5355 | 4.8999 | 96.6001 | 106.3999 | 0.9500 |
| total_injured | 126.5000 | 12.0208 | 16.6597 | 109.8403 | 143.1597 | 0.9500 |
| total_trapped | 177.0000 | 2.8284 | 3.9199 | 173.0801 | 180.9199 | 0.9500 |
| average_escape_time | 167.4300 | 3.3760 | 4.6788 | 162.7511 | 172.1088 | 0.9500 |

### Bootstrap Analysis Results

| Metric | metric | original_mean | bootstrap_mean | bootstrap_std | bootstrap_ci_lower | bootstrap_ci_upper |
|--------|--------|--------|--------|--------|--------|--------|
| 0 | total_evacuated | 186.5000 | 186.4900 | 0.3604 | 186.0000 | 187.0000 |
| 1 | total_dead | 101.5000 | 101.2500 | 1.7500 | 99.0000 | 104.0000 |
| 2 | total_trapped | 177.0000 | 176.9000 | 1.3379 | 175.0000 | 179.0000 |

## Conclusions

The Monte Carlo analysis provides robust statistical estimates of evacuation outcomes. Based on 2 successful simulations, the model predicts an average of 186.5 evacuated persons (95% CI: [185.5, 187.5]) and an average of 101.5 fatalities (95% CI: [96.6, 106.4]). The bootstrap analysis confirms the stability of these estimates.

