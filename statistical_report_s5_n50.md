# Statistical Analysis of the Evacuation Model

Generated: 2026-05-28 05:42:17

---

## Monte Carlo Methodology

This analysis performed 50 Monte Carlo simulations of Scenario 5 (Escenario 5 — Comportamiento grupal fuerte). Each simulation used a different random seed to ensure independence. The simulation ran for 300 timesteps (seconds).

## Simulation Configuration

- Scenario: 5
- Name: Escenario 5 — Comportamiento grupal fuerte
- Number of agents: 465
- Simulation steps: 300
- Follow group probability: 0.9
- Reaction time multiplier: 1.0

### Sample Statistics

| Metric | mean | variance | std_dev | min | max | median | q25 | q75 |
|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| total_evacuated | 188.0000 | 27.9184 | 5.2838 | 178.0000 | 199.0000 | 187.5000 | 184.2500 | 191.0000 |
| total_dead | 99.6200 | 19.5057 | 4.4165 | 87.0000 | 108.0000 | 100.0000 | 97.0000 | 102.7500 |
| total_injured | 123.7800 | 39.7261 | 6.3029 | 110.0000 | 139.0000 | 123.5000 | 119.0000 | 128.0000 |
| total_trapped | 177.3800 | 33.7506 | 5.8095 | 167.0000 | 189.0000 | 177.5000 | 174.0000 | 181.0000 |
| average_escape_time | 167.6586 | 9.4899 | 3.0806 | 161.8207 | 175.4500 | 167.8714 | 165.2296 | 169.3191 |
| max_density | 4.1312 | 0.0000 | 0.0000 | 4.1312 | 4.1312 | 4.1312 | 4.1312 | 4.1312 |
| average_smoke | 915.3483 | 115.5322 | 10.7486 | 893.8757 | 939.8720 | 915.9841 | 908.5565 | 922.8031 |

### 95% Confidence Intervals

| Metric | mean | std | margin_of_error | ci_lower | ci_upper | confidence_level |
|--------|--------|--------|--------|--------|--------|--------|
| total_evacuated | 188.0000 | 5.2838 | 1.4646 | 186.5354 | 189.4646 | 0.9500 |
| total_dead | 99.6200 | 4.4165 | 1.2242 | 98.3958 | 100.8442 | 0.9500 |
| total_injured | 123.7800 | 6.3029 | 1.7470 | 122.0330 | 125.5270 | 0.9500 |
| total_trapped | 177.3800 | 5.8095 | 1.6103 | 175.7697 | 178.9903 | 0.9500 |
| average_escape_time | 167.6586 | 3.0806 | 0.8539 | 166.8047 | 168.5125 | 0.9500 |

## Distribution Fitting

Distributions were fitted using Maximum Likelihood Estimation (MLE). The best-fitting distribution was selected based on Akaike Information Criterion (AIC).

### Distribution Fit Results

| Metric | metric | distribution | aic | bic | log_likelihood | best_fit |
|--------|--------|--------|--------|--------|--------|--------|
| 0 | total_evacuated | normal | 311.3480 | 315.1720 | -153.6740 | True |
| 1 | total_evacuated | lognormal | 313.1369 | 318.8730 | -153.5685 | False |
| 2 | total_evacuated | weibull | 320.6903 | 326.4263 | -157.3451 | False |
| 3 | total_dead | normal | 293.4191 | 297.2431 | -144.7095 | True |
| 4 | total_dead | lognormal | 296.5289 | 302.2650 | -145.2645 | False |
| 5 | total_dead | weibull | 294.9788 | 300.7148 | -144.4894 | False |
| 6 | average_escape_time | normal | 257.3949 | 261.2189 | -126.6974 | True |
| 7 | average_escape_time | lognormal | 259.1375 | 264.8735 | -126.5687 | False |
| 8 | average_escape_time | weibull | 270.3584 | 276.0944 | -132.1792 | False |

### Bootstrap Analysis Results

| Metric | metric | original_mean | bootstrap_mean | bootstrap_std | bootstrap_ci_lower | bootstrap_ci_upper |
|--------|--------|--------|--------|--------|--------|--------|
| 0 | total_evacuated | 188.0000 | 187.9810 | 0.7489 | 186.5395 | 189.4400 |
| 1 | total_dead | 99.6200 | 99.6301 | 0.6019 | 98.4590 | 100.8405 |
| 2 | total_trapped | 177.3800 | 177.3636 | 0.8258 | 175.8395 | 179.0000 |

## Conclusions

The Monte Carlo analysis provides robust statistical estimates of evacuation outcomes. Based on 50 successful simulations, the model predicts an average of 188.0 evacuated persons (95% CI: [186.5, 189.5]) and an average of 99.6 fatalities (95% CI: [98.4, 100.8]). The bootstrap analysis confirms the stability of these estimates.

