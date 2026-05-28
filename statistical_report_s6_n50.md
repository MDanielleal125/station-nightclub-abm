# Statistical Analysis of the Evacuation Model

Generated: 2026-05-28 06:17:52

---

## Monte Carlo Methodology

This analysis performed 50 Monte Carlo simulations of Scenario 6 (Escenario 6 — Reacción tardía). Each simulation used a different random seed to ensure independence. The simulation ran for 300 timesteps (seconds).

## Simulation Configuration

- Scenario: 6
- Name: Escenario 6 — Reacción tardía
- Number of agents: 465
- Simulation steps: 300
- Follow group probability: 0.65
- Reaction time multiplier: 2.0

### Sample Statistics

| Metric | mean | variance | std_dev | min | max | median | q25 | q75 |
|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| total_evacuated | 144.4400 | 33.4351 | 5.7823 | 129.0000 | 154.0000 | 145.0000 | 140.2500 | 148.7500 |
| total_dead | 155.8200 | 74.3955 | 8.6253 | 141.0000 | 187.0000 | 154.0000 | 151.0000 | 161.0000 |
| total_injured | 182.3600 | 94.3984 | 9.7159 | 162.0000 | 203.0000 | 181.5000 | 178.0000 | 188.7500 |
| total_trapped | 164.7400 | 81.8290 | 9.0459 | 127.0000 | 184.0000 | 165.0000 | 160.2500 | 169.7500 |
| average_escape_time | 188.7006 | 16.8866 | 4.1093 | 180.5436 | 196.7698 | 188.9839 | 185.5467 | 191.7785 |
| max_density | 4.1312 | 0.0000 | 0.0000 | 4.1312 | 4.1312 | 4.1312 | 4.1312 | 4.1312 |
| average_smoke | 917.5534 | 172.5904 | 13.1374 | 889.1742 | 952.3575 | 917.7035 | 910.6854 | 926.5083 |

### 95% Confidence Intervals

| Metric | mean | std | margin_of_error | ci_lower | ci_upper | confidence_level |
|--------|--------|--------|--------|--------|--------|--------|
| total_evacuated | 144.4400 | 5.7823 | 1.6027 | 142.8373 | 146.0427 | 0.9500 |
| total_dead | 155.8200 | 8.6253 | 2.3908 | 153.4292 | 158.2108 | 0.9500 |
| total_injured | 182.3600 | 9.7159 | 2.6931 | 179.6669 | 185.0531 | 0.9500 |
| total_trapped | 164.7400 | 9.0459 | 2.5074 | 162.2326 | 167.2474 | 0.9500 |
| average_escape_time | 188.7006 | 4.1093 | 1.1390 | 187.5616 | 189.8396 | 0.9500 |

## Distribution Fitting

Distributions were fitted using Maximum Likelihood Estimation (MLE). The best-fitting distribution was selected based on Akaike Information Criterion (AIC).

### Distribution Fit Results

| Metric | metric | distribution | aic | bic | log_likelihood | best_fit |
|--------|--------|--------|--------|--------|--------|--------|
| 0 | total_evacuated | normal | 320.3640 | 324.1881 | -158.1820 | True |
| 1 | total_evacuated | lognormal | 323.3658 | 329.1018 | -158.6829 | False |
| 2 | total_evacuated | weibull | 321.2980 | 327.0341 | -157.6490 | False |
| 3 | total_dead | normal | 360.3535 | 364.1775 | -178.1767 | False |
| 4 | total_dead | lognormal | 360.2443 | 365.9804 | -177.1221 | True |
| 5 | total_dead | weibull | 380.4114 | 386.1475 | -187.2057 | False |
| 6 | average_escape_time | normal | 286.2099 | 290.0339 | -141.1049 | True |
| 7 | average_escape_time | lognormal | 288.2742 | 294.0103 | -141.1371 | False |
| 8 | average_escape_time | weibull | 292.3471 | 298.0832 | -143.1736 | False |

### Bootstrap Analysis Results

| Metric | metric | original_mean | bootstrap_mean | bootstrap_std | bootstrap_ci_lower | bootstrap_ci_upper |
|--------|--------|--------|--------|--------|--------|--------|
| 0 | total_evacuated | 144.4400 | 144.4333 | 0.8079 | 142.9000 | 146.0000 |
| 1 | total_dead | 155.8200 | 155.7744 | 1.2057 | 153.6190 | 158.3000 |
| 2 | total_trapped | 164.7400 | 164.7150 | 1.2493 | 162.1795 | 166.8800 |

## Conclusions

The Monte Carlo analysis provides robust statistical estimates of evacuation outcomes. Based on 50 successful simulations, the model predicts an average of 144.4 evacuated persons (95% CI: [142.8, 146.0]) and an average of 155.8 fatalities (95% CI: [153.4, 158.2]). The bootstrap analysis confirms the stability of these estimates.

