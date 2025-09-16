from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize
import numpy as np

def required_sample_size_for_proportions(baseline_rate, mde_abs, alpha=0.05, power=0.8, alternative='two-sided'):
    """
    return (n_per_group, n_total, effect_size_Cohen_h)
    baseline_rate: control conversion rate (e.g., 0.10)
    mde_abs: absolute difference to detect (e.g., 0.02 means detect 12% vs 10%)
    alpha: significance level (default 0.05)
    power: desired power (default 0.8)
    alternative: 'two-sided' or 'one-sided'
    """
    p1 = baseline_rate
    p2 = baseline_rate + mde_abs
    if not (0 < p1 < 1):
        raise ValueError("baseline_rate must be between 0 and 1 (exclusive).")
    if not (0 < p2 < 1):
        raise ValueError("p2 (baseline_rate + mde_abs) must be between 0 and 1 (exclusive).") 
    effect_size = proportion_effectsize(p2, p1)  # Cohen's h
    analysis = NormalIndPower()
    n_per_group = analysis.solve_power(effect_size=abs(effect_size), power=power, alpha=alpha, alternative=alternative)
    return int(np.ceil(n_per_group)), int(np.ceil(2*n_per_group)), effect_size

def print_custom(baseline_rate, mde_abs, alpha=0.05, power=0.8, alternative='two-sided'):
  n_per, n_total, eff = required_sample_size_for_proportions(baseline_rate, mde_abs, alpha, power, alternative)
  p1 = baseline_rate
  p2 = p1 + mde_abs
  print(f"Baseline {p1:.2%} -> Target {p2:.2%} | alpha={alpha}, power={power}, alt={alternative}")
  print(f"Effect size (Cohen's h) = {eff:.6f}")
  print(f"Required sample size per group = {n_per:,}, Total = {n_total:,}\n")

if __name__ == "__main__":
  scenarios = [
    (0.10, 0.02, 0.05, 0.8, 'two-sided'),
    (0.20, 0.02, 0.05, 0.8, 'two-sided'),
    (0.10, 0.01, 0.05, 0.8, 'two-sided'),
    (0.05, 0.01, 0.05, 0.8, 'two-sided'),
    (0.10, 0.02, 0.05, 0.9, 'two-sided'),
  ]
  for s in scenarios:
    print_custom(*s)

