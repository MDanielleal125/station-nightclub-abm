# Statistical Analysis of the Evacuation Model

Generated: 2026-05-28 04:19:40

---

## Monte Carlo Methodology

This analysis performed 50 Monte Carlo simulations of Scenario 3 (Escenario 3 — Más humo). Each simulation used a different random seed to ensure independence. The simulation ran for 300 timesteps (seconds).

## Simulation Configuration

- Scenario: 3
- Name: Escenario 3 — Más humo
- Number of agents: 465
- Simulation steps: 300
- Follow group probability: 0.65
- Reaction time multiplier: 1.0

### Sample Statistics

| Metric | mean | variance | std_dev | min | max | median | q25 | q75 |
|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| total_evacuated | 184.7000 | 42.8673 | 6.5473 | 170.0000 | 198.0000 | 185.0000 | 181.2500 | 189.0000 |
| total_dead | 119.9600 | 33.9576 | 5.8273 | 106.0000 | 133.0000 | 120.5000 | 116.0000 | 124.0000 |
| total_injured | 148.9200 | 71.5853 | 8.4608 | 131.0000 | 170.0000 | 148.5000 | 143.0000 | 153.0000 |
| total_trapped | 160.3400 | 42.8820 | 6.5484 | 149.0000 | 177.0000 | 160.0000 | 155.0000 | 166.0000 |
| average_escape_time | 165.4770 | 12.2043 | 3.4935 | 158.3069 | 173.0281 | 165.3756 | 163.2548 | 167.9540 |
| max_density | 4.1312 | 0.0000 | 0.0000 | 4.1312 | 4.1312 | 4.1312 | 4.1312 | 4.1312 |
| average_smoke | 1004.1552 | 193.7520 | 13.9195 | 965.0302 | 1033.5198 | 1006.5397 | 996.0387 | 1012.7521 |

### 95% Confidence Intervals

| Metric | mean | std | margin_of_error | ci_lower | ci_upper | confidence_level |
|--------|--------|--------|--------|--------|--------|--------|
| total_evacuated | 184.7000 | 6.5473 | 1.8148 | 182.8852 | 186.5148 | 0.9500 |
| total_dead | 119.9600 | 5.8273 | 1.6152 | 118.3448 | 121.5752 | 0.9500 |
| total_injured | 148.9200 | 8.4608 | 2.3452 | 146.5748 | 151.2652 | 0.9500 |
| total_trapped | 160.3400 | 6.5484 | 1.8151 | 158.5249 | 162.1551 | 0.9500 |
| average_escape_time | 165.4770 | 3.4935 | 0.9683 | 164.5086 | 166.4453 | 0.9500 |

## Distribution Fitting

Distributions were fitted using Maximum Likelihood Estimation (MLE). The best-fitting distribution was selected based on Akaike Information Criterion (AIC).

### Distribution Fit Results

| Metric | metric | distribution | aic | bic | log_likelihood | best_fit |
|--------|--------|--------|--------|--------|--------|--------|
| 0 | total_evacuated | normal | 332.7892 | 336.6133 | -164.3946 | True |
| 1 | total_evacuated | lognormal | 335.2011 | 340.9371 | -164.6005 | False |
| 2 | total_evacuated | weibull | 337.5223 | 343.2584 | -165.7611 | False |
| 3 | total_dead | normal | 321.1393 | 324.9633 | -158.5696 | True |
| 4 | total_dead | lognormal | 323.3284 | 329.0644 | -158.6642 | False |
| 5 | total_dead | weibull | 327.6437 | 333.3798 | -160.8219 | False |
| 6 | average_escape_time | normal | 269.9733 | 273.7973 | -132.9866 | True |
| 7 | average_escape_time | lognormal | 272.0660 | 277.8020 | -133.0330 | False |
| 8 | average_escape_time | weibull | 275.9812 | 281.7172 | -134.9906 | False |

### Bootstrap Analysis Results

| Metric | metric | original_mean | bootstrap_mean | bootstrap_std | bootstrap_ci_lower | bootstrap_ci_upper |
|--------|--------|--------|--------|--------|--------|--------|
| 0 | total_evacuated | 184.7000 | 184.7122 | 0.9053 | 182.9195 | 186.5200 |
| 1 | total_dead | 119.9600 | 119.9611 | 0.8098 | 118.2795 | 121.4600 |
| 2 | total_trapped | 160.3400 | 160.3191 | 0.8891 | 158.5400 | 161.9600 |

## Conclusions

The Monte Carlo analysis provides robust statistical estimates of evacuation outcomes. Based on 50 successful simulations, the model predicts an average of 184.7 evacuated persons (95% CI: [182.9, 186.5]) and an average of 120.0 fatalities (95% CI: [118.3, 121.6]). The bootstrap analysis confirms the stability of these estimates.

