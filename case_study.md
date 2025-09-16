# A/B Testing Case Study

## How to increate Youtube watch time (end to end plan)?
Let's say the change is redesigning the "next up" thumbnails to autoplay from user's recent watch history rather than the current generic content.  

**1. Goal & Hypothesis**  
Goal: increase the average watch time per user session by 2mins with baseline as 20mins.  
Hypothesis: autoplay from recent watch history will increase the average watch time vs. generic thumbnails.  
Primary metric: averge watch time per use session.  
Secondary metrics: CTR; session length; average watch time per "next up" video.  
Guardrail metrics: RPM; unsubscribe rate; users complaints.  

**2. Experiment Design**  
Control(A): current thumbnails with generic content.  
Treatment(B): redesigned thumbnails with recent watch history.  
Randomization: user-level, consistent across devices.  
Duration: at least 1-2 user cycles, usually 7-14 days.  

**3. Sample size calculation**  
Since the success metric is continuous, we are using t-test power analysis to calculate the sample size.  
-- code --:    
```
from statsmodels.stats.power import TTestIndPower
import numpy as np

# Initialize power analysis object
analysis = TTestIndPower()

# Parameters (example for YouTube watch time)
alpha = 0.05        # significance level
power = 0.8         # 80% power
baseline_mean = 20  # average minutes of watch time
sigma = 30          # standard deviation of watch time
delta = 2           # minimum detectable effect (in minutes)

# Standardized effect size (Cohen's d)
effect_size = delta / sigma

# Calculate required sample size per group
sample_size = analysis.solve_power(effect_size=effect_size,
                                   alpha=alpha,
                                   power=power,
                                   alternative='two-sided')

print(f"Required sample size per group: {np.ceil(sample_size):,.0f}")
print(f"Total sample size: {np.ceil(sample_size*2):,.0f}")
```
-- result --:  
```
Required sample size per group: 3,528
Total sample size: 7,056
```  
If the metric is binary or proportion, we use z-test power analysis to do the calculation.  
code ref: [z-test](https://github.com/zhengyiling/Data-Science/blob/main/required_sample_size_for_proportions.py)  

**4. Implementation**  
- Roll out treatment only to assigned users.
- Ensure only the testing feature differs.
- Track required metrics via experiment logging.

**5. Analysis & Interpretation**  
a. pull data for statistical tests.  
-- primary metric sql code --: 
```
-- Step 1: Pull user-level aggregated watch time
WITH user_sessions AS (
    SELECT
        user_id,
        variant,  -- 'A' = control, 'B' = treatment
        DATE(event_time) AS event_date,
        SUM(watch_minutes) AS total_watch_time,
        COUNT(DISTINCT video_id) AS num_videos
    FROM video_watch_events
    WHERE event_time BETWEEN '2025-09-01' AND '2025-09-14'
    GROUP BY user_id, variant, DATE(event_time)
)
-- Step 2: Aggregate to user-level (primary metric = avg daily watch time)
SELECT
    variant,
    AVG(total_watch_time) AS avg_watch_time_per_user,
    STDDEV(total_watch_time) AS std_watch_time,
    COUNT(DISTINCT user_id) AS n_users
FROM user_sessions
GROUP BY variant;
```
b. run statistical tests to compute p-value and CI for delta(uplift).  
- decision rule: reject H0 if p < 0.05 and CI excludes 0.

c. do guardrails check to ensure no negative side effects(churn, revenue drop).  

**6. Decision & Next Steps**  
- Rollout: if the result is statistically significant, and no harm to guardrails.  
- Iterate: if trend positive but not significant.  
- Reject: if no effect or harmful impact.  
- Avoid pitfalls: Novelty effect, seasonality bias, peeking early, metric misalignment.  




