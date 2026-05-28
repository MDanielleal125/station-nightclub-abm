# Statistical Analysis of the Evacuation Model

Generated: 2026-05-28 03:38:38

---

## Monte Carlo Methodology

This analysis performed 50 Monte Carlo simulations of Scenario 2 (Escenario 2 — Alta congestión). Each simulation used a different random seed to ensure independence. The simulation ran for 300 timesteps (seconds).

## Simulation Configuration

- Scenario: 2
- Name: Escenario 2 — Alta congestión
- Number of agents: 700
- Simulation steps: 300
- Follow group probability: 0.65
- Reaction time multiplier: 1.0

### Sample Statistics

| Metric | mean | variance | std_dev | min | max | median | q25 | q75 |
|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| total_evacuated | 190.3600 | 93.1739 | 9.6527 | 169.0000 | 216.0000 | 190.0000 | 183.2500 | 197.0000 |
| total_dead | 249.0200 | 108.0608 | 10.3952 | 228.0000 | 271.0000 | 249.0000 | 242.0000 | 256.7500 |
| total_injured | 347.5400 | 269.5596 | 16.4183 | 317.0000 | 393.0000 | 346.0000 | 337.0000 | 358.5000 |
| total_trapped | 260.6200 | 81.3424 | 9.0190 | 238.0000 | 281.0000 | 261.0000 | 255.2500 | 267.0000 |
| average_escape_time | 160.1281 | 14.9381 | 3.8650 | 149.9842 | 169.4509 | 159.9164 | 157.8964 | 162.1539 |
| max_density | 5.8974 | 0.0183 | 0.1354 | 5.6257 | 6.2286 | 5.8892 | 5.8143 | 5.9843 |
| average_smoke | 913.3174 | 186.3778 | 13.6520 | 879.9083 | 942.4717 | 913.9564 | 904.3147 | 923.0238 |

### 95% Confidence Intervals

| Metric | mean | std | margin_of_error | ci_lower | ci_upper | confidence_level |
|--------|--------|--------|--------|--------|--------|--------|
| total_evacuated | 190.3600 | 9.6527 | 2.6755 | 187.6845 | 193.0355 | 0.9500 |
| total_dead | 249.0200 | 10.3952 | 2.8814 | 246.1386 | 251.9014 | 0.9500 |
| total_injured | 347.5400 | 16.4183 | 4.5508 | 342.9892 | 352.0908 | 0.9500 |
| total_trapped | 260.6200 | 9.0190 | 2.4999 | 258.1201 | 263.1199 | 0.9500 |
| average_escape_time | 160.1281 | 3.8650 | 1.0713 | 159.0568 | 161.1994 | 0.9500 |

## Distribution Fitting

Distributions were fitted using Maximum Likelihood Estimation (MLE). The best-fitting distribution was selected based on Akaike Information Criterion (AIC).

### Distribution Fit Results

| Metric | metric | distribution | aic | bic | log_likelihood | best_fit |
|--------|--------|--------|--------|--------|--------|--------|
| 0 | total_evacuated | normal | 371.6071 | 375.4311 | -183.8035 | True |
| 1 | total_evacuated | lognormal | 373.2679 | 379.0040 | -183.6339 | False |
| 2 | total_evacuated | weibull | 381.9674 | 387.7035 | -187.9837 | False |
| 3 | total_dead | normal | 379.0184 | 382.8425 | -187.5092 | True |
| 4 | total_dead | lognormal | 381.0741 | 386.8102 | -187.5371 | False |
| 5 | total_dead | weibull | 385.1173 | 390.8534 | -189.5587 | False |
| 6 | average_escape_time | normal | 280.0796 | 283.9037 | -138.0398 | True |
| 7 | average_escape_time | lognormal | 282.1523 | 287.8884 | -138.0762 | False |
| 8 | average_escape_time | weibull | 289.3910 | 295.1271 | -141.6955 | False |

### Bootstrap Analysis Results

| Metric | metric | original_mean | bootstrap_mean | bootstrap_std | bootstrap_ci_lower | bootstrap_ci_upper |
|--------|--------|--------|--------|--------|--------|--------|
| 0 | total_evacuated | 190.3600 | 190.2574 | 1.3643 | 187.7000 | 192.8410 |
| 1 | total_dead | 249.0200 | 249.0134 | 1.4569 | 246.1600 | 251.9005 |
| 2 | total_trapped | 260.6200 | 260.6899 | 1.2371 | 258.2800 | 263.1000 |

## Conclusions

The Monte Carlo analysis provides robust statistical estimates of evacuation outcomes. Based on 50 successful simulations, the model predicts an average of 190.4 evacuated persons (95% CI: [187.7, 193.0]) and an average of 249.0 fatalities (95% CI: [246.1, 251.9]). The bootstrap analysis confirms the stability of these estimates.

