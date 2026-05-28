# Statistical Analysis of the Evacuation Model

Generated: 2026-05-28 02:36:19

---

## Monte Carlo Methodology

This analysis performed 50 Monte Carlo simulations of Scenario 1 (Escenario 1 — Base). Each simulation used a different random seed to ensure independence. The simulation ran for 300 timesteps (seconds).

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
| total_evacuated | 187.9200 | 26.1159 | 5.1104 | 178.0000 | 199.0000 | 188.0000 | 184.2500 | 191.0000 |
| total_dead | 99.5800 | 19.3506 | 4.3989 | 87.0000 | 108.0000 | 100.0000 | 97.0000 | 102.7500 |
| total_injured | 123.6400 | 40.4392 | 6.3592 | 110.0000 | 139.0000 | 123.0000 | 119.0000 | 128.0000 |
| total_trapped | 177.5000 | 32.2143 | 5.6758 | 167.0000 | 189.0000 | 177.5000 | 174.0000 | 181.0000 |
| average_escape_time | 167.6533 | 9.3111 | 3.0514 | 161.8207 | 175.4500 | 167.8714 | 165.7175 | 169.0443 |
| max_density | 4.1312 | 0.0000 | 0.0000 | 4.1312 | 4.1312 | 4.1312 | 4.1312 | 4.1312 |
| average_smoke | 915.6770 | 107.1239 | 10.3501 | 893.8757 | 939.8720 | 915.9841 | 910.2044 | 922.8031 |

### 95% Confidence Intervals

| Metric | mean | std | margin_of_error | ci_lower | ci_upper | confidence_level |
|--------|--------|--------|--------|--------|--------|--------|
| total_evacuated | 187.9200 | 5.1104 | 1.4165 | 186.5035 | 189.3365 | 0.9500 |
| total_dead | 99.5800 | 4.3989 | 1.2193 | 98.3607 | 100.7993 | 0.9500 |
| total_injured | 123.6400 | 6.3592 | 1.7626 | 121.8774 | 125.4026 | 0.9500 |
| total_trapped | 177.5000 | 5.6758 | 1.5732 | 175.9268 | 179.0732 | 0.9500 |
| average_escape_time | 167.6533 | 3.0514 | 0.8458 | 166.8075 | 168.4991 | 0.9500 |

## Distribution Fitting

Distributions were fitted using Maximum Likelihood Estimation (MLE). The best-fitting distribution was selected based on Akaike Information Criterion (AIC).

### Distribution Fit Results

| Metric | metric | distribution | aic | bic | log_likelihood | best_fit |
|--------|--------|--------|--------|--------|--------|--------|
| 0 | total_evacuated | normal | 308.0110 | 311.8350 | -152.0055 | True |
| 1 | total_evacuated | lognormal | 309.9116 | 315.6476 | -151.9558 | False |
| 2 | total_evacuated | weibull | 316.7114 | 322.4474 | -155.3557 | False |
| 3 | total_dead | normal | 293.0199 | 296.8440 | -144.5100 | True |
| 4 | total_dead | lognormal | 296.1173 | 301.8534 | -145.0587 | False |
| 5 | total_dead | weibull | 294.6960 | 300.4320 | -144.3480 | False |
| 6 | average_escape_time | normal | 256.4440 | 260.2681 | -126.2220 | True |
| 7 | average_escape_time | lognormal | 258.1743 | 263.9103 | -126.0871 | False |
| 8 | average_escape_time | weibull | 269.8694 | 275.6055 | -131.9347 | False |

### Bootstrap Analysis Results

| Metric | metric | original_mean | bootstrap_mean | bootstrap_std | bootstrap_ci_lower | bootstrap_ci_upper |
|--------|--------|--------|--------|--------|--------|--------|
| 0 | total_evacuated | 187.9200 | 187.8969 | 0.7263 | 186.4000 | 189.3405 |
| 1 | total_dead | 99.5800 | 99.5915 | 0.5979 | 98.4000 | 100.7605 |
| 2 | total_trapped | 177.5000 | 177.4840 | 0.8092 | 175.9595 | 179.0805 |

## Conclusions

The Monte Carlo analysis provides robust statistical estimates of evacuation outcomes. Based on 50 successful simulations, the model predicts an average of 187.9 evacuated persons (95% CI: [186.5, 189.3]) and an average of 99.6 fatalities (95% CI: [98.4, 100.8]). The bootstrap analysis confirms the stability of these estimates.

