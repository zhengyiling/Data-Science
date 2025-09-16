# A/B Testing Case Study

## How to increate Youtube watch time (end to end plan)?

**1. Hypothesis formulation**  
Let's say the change is redesigning the "next up" thumbnails to autoplay personalized user's recent watch history rather than the current generic content. The goal is to increase the average watch time per unique user over a 24hrs session for 2 minutes with the baseline 20 minutes. So the hypothesis is personalized autoplay thumbnails will increase the average watch time per user over a session by 10%.
- Null hypothesis: personalized autoplay thumbnails would not extend the watch time of users per session.  
- Alternative hypothesis: with the personalized autoplay thumbnails, the average watch time increased by at least the MDE.

**2. Target metrics definition**  
The primary metric is the average watch time per unique user over a 24hrs session.  
The secondary metrics can be the CTR on the "next up" thumbnails, the numbers of videos watched per session and session RPM.
The guardrail metric can be user compliants, unsubscribe rate and increase in errors.

**3. Sample size calculation**
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
```
# pip install statsmodels if not installed
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

```
Required sample size per group: 3,528
Total sample size: 7,056
```
**4. Rondomization strategy**
**5. Control group design**


