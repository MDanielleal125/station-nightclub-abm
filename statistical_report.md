# Statistical Analysis of the Evacuation Model

Generated: 2026-05-28 01:20:43

---

## Monte Carlo Methodology

This analysis performed 1 Monte Carlo simulations of Scenario 6 (Escenario 6 — Reacción tardía). Each simulation used a different random seed to ensure independence. The simulation ran for 300 timesteps (seconds).

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
| total_evacuated | 146.0000 | nan | nan | 146.0000 | 146.0000 | 146.0000 | 146.0000 | 146.0000 |
| total_dead | 154.0000 | nan | nan | 154.0000 | 154.0000 | 154.0000 | 154.0000 | 154.0000 |
| total_injured | 180.0000 | nan | nan | 180.0000 | 180.0000 | 180.0000 | 180.0000 | 180.0000 |
| total_trapped | 165.0000 | nan | nan | 165.0000 | 165.0000 | 165.0000 | 165.0000 | 165.0000 |
| average_escape_time | 187.5479 | nan | nan | 187.5479 | 187.5479 | 187.5479 | 187.5479 | 187.5479 |
| max_density | 4.1312 | nan | nan | 4.1312 | 4.1312 | 4.1312 | 4.1312 | 4.1312 |
| average_smoke | 919.9307 | nan | nan | 919.9307 | 919.9307 | 919.9307 | 919.9307 | 919.9307 |

### 95% Confidence Intervals

| Metric | mean | std | margin_of_error | ci_lower | ci_upper | confidence_level |
|--------|--------|--------|--------|--------|--------|--------|
| total_evacuated | 146.0000 | nan | nan | nan | nan | 0.9500 |
| total_dead | 154.0000 | nan | nan | nan | nan | 0.9500 |
| total_injured | 180.0000 | nan | nan | nan | nan | 0.9500 |
| total_trapped | 165.0000 | nan | nan | nan | nan | 0.9500 |
| average_escape_time | 187.5479 | nan | nan | nan | nan | 0.9500 |

### Bootstrap Analysis Results

| Metric | metric | original_mean | bootstrap_mean | bootstrap_std | bootstrap_ci_lower | bootstrap_ci_upper |
|--------|--------|--------|--------|--------|--------|--------|
| 0 | total_evacuated | 146.0000 | 146.0000 | 0.0000 | 146.0000 | 146.0000 |
| 1 | total_dead | 154.0000 | 154.0000 | 0.0000 | 154.0000 | 154.0000 |
| 2 | total_trapped | 165.0000 | 165.0000 | 0.0000 | 165.0000 | 165.0000 |

## Conclusions

The Monte Carlo analysis provides robust statistical estimates of evacuation outcomes. Based on 1 successful simulations, the model predicts an average of 146.0 evacuated persons (95% CI: [nan, nan]) and an average of 154.0 fatalities (95% CI: [nan, nan]). The bootstrap analysis confirms the stability of these estimates.

