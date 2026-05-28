# Statistical Analysis of the Evacuation Model

Generated: 2026-05-28 03:40:38

---

## Monte Carlo Methodology

This analysis performed 100 Monte Carlo simulations of Scenario 1 (Escenario 1 — Base). Each simulation used a different random seed to ensure independence. The simulation ran for 300 timesteps (seconds).

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
| total_evacuated | 183.8100 | 48.1757 | 6.9409 | 169.0000 | 202.0000 | 184.0000 | 179.0000 | 187.2500 |
| total_dead | 99.6400 | 23.2024 | 4.8169 | 85.0000 | 110.0000 | 100.0000 | 96.0000 | 103.0000 |
| total_injured | 124.2100 | 42.3292 | 6.5061 | 105.0000 | 141.0000 | 124.0000 | 120.0000 | 128.0000 |
| total_trapped | 181.5500 | 45.7247 | 6.7620 | 166.0000 | 198.0000 | 181.0000 | 177.0000 | 186.0000 |
| average_escape_time | 167.9295 | 11.9107 | 3.4512 | 159.2194 | 174.7865 | 167.7326 | 165.6972 | 170.3957 |
| max_density | 4.1312 | 0.0000 | 0.0000 | 4.1312 | 4.1312 | 4.1312 | 4.1312 | 4.1312 |
| average_smoke | 915.8878 | 196.0614 | 14.0022 | 870.3625 | 943.1665 | 915.5331 | 908.3223 | 924.0974 |

### 95% Confidence Intervals

| Metric | mean | std | margin_of_error | ci_lower | ci_upper | confidence_level |
|--------|--------|--------|--------|--------|--------|--------|
| total_evacuated | 183.8100 | 6.9409 | 1.3604 | 182.4496 | 185.1704 | 0.9500 |
| total_dead | 99.6400 | 4.8169 | 0.9441 | 98.6959 | 100.5841 | 0.9500 |
| total_injured | 124.2100 | 6.5061 | 1.2752 | 122.9348 | 125.4852 | 0.9500 |
| total_trapped | 181.5500 | 6.7620 | 1.3253 | 180.2247 | 182.8753 | 0.9500 |
| average_escape_time | 167.9295 | 3.4512 | 0.6764 | 167.2531 | 168.6059 | 0.9500 |

## Distribution Fitting

Distributions were fitted using Maximum Likelihood Estimation (MLE). The best-fitting distribution was selected based on Akaike Information Criterion (AIC).

### Distribution Fit Results

| Metric | metric | distribution | aic | bic | log_likelihood | best_fit |
|--------|--------|--------|--------|--------|--------|--------|
| 0 | total_evacuated | normal | 674.2681 | 679.4784 | -335.1340 | True |
| 1 | total_evacuated | lognormal | 675.2706 | 683.0861 | -334.6353 | False |
| 2 | total_evacuated | weibull | 694.9001 | 702.7156 | -344.4501 | False |
| 3 | total_dead | normal | 601.2083 | 606.4187 | -298.6042 | True |
| 4 | total_dead | lognormal | 605.3183 | 613.1338 | -299.6591 | False |
| 5 | total_dead | weibull | 603.6187 | 611.4342 | -298.8094 | False |
| 6 | average_escape_time | normal | 534.5264 | 539.7367 | -265.2632 | True |
| 7 | average_escape_time | lognormal | 536.8440 | 544.6595 | -265.4220 | False |
| 8 | average_escape_time | weibull | 542.4874 | 550.3029 | -268.2437 | False |

### Bootstrap Analysis Results

| Metric | metric | original_mean | bootstrap_mean | bootstrap_std | bootstrap_ci_lower | bootstrap_ci_upper |
|--------|--------|--------|--------|--------|--------|--------|
| 0 | total_evacuated | 183.8100 | 183.7988 | 0.6706 | 182.5200 | 185.1200 |
| 1 | total_dead | 99.6400 | 99.6326 | 0.4567 | 98.7195 | 100.4702 |
| 2 | total_trapped | 181.5500 | 181.5717 | 0.6769 | 180.2698 | 182.8900 |

## Conclusions

The Monte Carlo analysis provides robust statistical estimates of evacuation outcomes. Based on 100 successful simulations, the model predicts an average of 183.8 evacuated persons (95% CI: [182.4, 185.2]) and an average of 99.6 fatalities (95% CI: [98.7, 100.6]). The bootstrap analysis confirms the stability of these estimates.

