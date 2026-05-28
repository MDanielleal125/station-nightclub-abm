# Statistical Analysis of the Evacuation Model

Generated: 2026-05-28 05:00:03

---

## Monte Carlo Methodology

This analysis performed 50 Monte Carlo simulations of Scenario 4 (Escenario 4 — Salidas bloqueadas). Each simulation used a different random seed to ensure independence. The simulation ran for 300 timesteps (seconds).

## Simulation Configuration

- Scenario: 4
- Name: Escenario 4 — Salidas bloqueadas
- Number of agents: 465
- Simulation steps: 300
- Follow group probability: 0.65
- Reaction time multiplier: 1.0

### Sample Statistics

| Metric | mean | variance | std_dev | min | max | median | q25 | q75 |
|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| total_evacuated | 186.4000 | 41.8776 | 6.4713 | 168.0000 | 201.0000 | 186.5000 | 182.0000 | 191.0000 |
| total_dead | 100.9200 | 18.1976 | 4.2659 | 90.0000 | 109.0000 | 100.5000 | 98.0000 | 103.7500 |
| total_injured | 124.8400 | 55.4841 | 7.4488 | 106.0000 | 148.0000 | 126.0000 | 120.0000 | 129.0000 |
| total_trapped | 177.6800 | 33.8139 | 5.8150 | 161.0000 | 190.0000 | 177.0000 | 175.0000 | 181.0000 |
| average_escape_time | 168.1291 | 10.7515 | 3.2789 | 161.7382 | 175.3869 | 168.1873 | 165.8372 | 170.8215 |
| max_density | 4.1312 | 0.0000 | 0.0000 | 4.1312 | 4.1312 | 4.1312 | 4.1312 | 4.1312 |
| average_smoke | 917.5274 | 125.0933 | 11.1845 | 890.7873 | 954.3209 | 917.3419 | 910.9181 | 923.4793 |

### 95% Confidence Intervals

| Metric | mean | std | margin_of_error | ci_lower | ci_upper | confidence_level |
|--------|--------|--------|--------|--------|--------|--------|
| total_evacuated | 186.4000 | 6.4713 | 1.7937 | 184.6063 | 188.1937 | 0.9500 |
| total_dead | 100.9200 | 4.2659 | 1.1824 | 99.7376 | 102.1024 | 0.9500 |
| total_injured | 124.8400 | 7.4488 | 2.0647 | 122.7753 | 126.9047 | 0.9500 |
| total_trapped | 177.6800 | 5.8150 | 1.6118 | 176.0682 | 179.2918 | 0.9500 |
| average_escape_time | 168.1291 | 3.2789 | 0.9089 | 167.2203 | 169.0380 | 0.9500 |

## Distribution Fitting

Distributions were fitted using Maximum Likelihood Estimation (MLE). The best-fitting distribution was selected based on Akaike Information Criterion (AIC).

### Distribution Fit Results

| Metric | metric | distribution | aic | bic | log_likelihood | best_fit |
|--------|--------|--------|--------|--------|--------|--------|
| 0 | total_evacuated | normal | 331.6212 | 335.4453 | -163.8106 | True |
| 1 | total_evacuated | lognormal | 334.0653 | 339.8014 | -164.0327 | False |
| 2 | total_evacuated | weibull | 338.1599 | 343.8960 | -166.0800 | False |
| 3 | total_dead | normal | 289.9481 | 293.7721 | -142.9740 | True |
| 4 | total_dead | lognormal | 291.9202 | 297.6563 | -142.9601 | False |
| 5 | total_dead | weibull | 297.3108 | 303.0469 | -145.6554 | False |
| 6 | average_escape_time | normal | 263.6358 | 267.4598 | -129.8179 | True |
| 7 | average_escape_time | lognormal | 265.7796 | 271.5157 | -129.8898 | False |
| 8 | average_escape_time | weibull | 268.0482 | 273.7843 | -131.0241 | False |

### Bootstrap Analysis Results

| Metric | metric | original_mean | bootstrap_mean | bootstrap_std | bootstrap_ci_lower | bootstrap_ci_upper |
|--------|--------|--------|--------|--------|--------|--------|
| 0 | total_evacuated | 186.4000 | 186.4202 | 0.9193 | 184.6400 | 188.2805 |
| 1 | total_dead | 100.9200 | 100.9272 | 0.5962 | 99.8200 | 102.1405 |
| 2 | total_trapped | 177.6800 | 177.6841 | 0.8041 | 176.1395 | 179.2600 |

## Conclusions

The Monte Carlo analysis provides robust statistical estimates of evacuation outcomes. Based on 50 successful simulations, the model predicts an average of 186.4 evacuated persons (95% CI: [184.6, 188.2]) and an average of 100.9 fatalities (95% CI: [99.7, 102.1]). The bootstrap analysis confirms the stability of these estimates.

