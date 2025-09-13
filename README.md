# Basic A/B Testing Questions  

## Understanding A/B Test  

**What is A/B testing?**  
A/B tesing is an experimental method used to compare two versions of a product feature to see which one performs better against a defined goal.

**How to explain A/B testing to a non-technical stakeholder?**  
A/B testing is a way to run an experiment where we compare two versions of a product feature. There will be two groups of users, control group and treatment group. 
The control group sees the current version, and the treatment group sees the new version with the change. The only difference between the two is the feature we want to test. 
Then we track a key metric — like click-through rate or sign-ups — to see if the new version leads to better results. 
If the difference is big enough, and it’s unlikely caused by chance, we can then confidently decide whether to roll out the new change.

**Why use A/B Testing?**  
1. It helps the company to make data-driven decisions to grow the business and not just rely on guesswork or opinions.
2. It can help the company better understand the users by analyzing how they behave to the certain changes, and from there the user experience could be optimized properly.
   
**What is the framework of A/B Testing?**  
1. Start with a clear hypothesis.
2. Pick metrics: primary(success), secondary, guardrails. (conversation rate, CTR, revenue per visitor, average watch time)
3. Design variants and allocation (population, randomization, blocking/stratification)
4. Calculate sample size, power, and test duration; set stopping rules
5. Implement changes and instrument tracking; run QA
6. Launch and monitor health metrics (no early peeking)
7. Analyze results (appropriate statistical test, p-values, effect size, CIs, subgroup checks)
8. Decide: roll out, iterate, or rollback
9. Document results & learnings for future tests

## Designing A/B Test

**How do you determine the sample size for an A/B test?**  
To calculate the sample size for an A/B test, I’d use power analysis. The key inputs are:
1. Baseline rate of the current performance of the metric, like conversion rate
2. Minimum detectable effect, the smallest change worth detecting
3. Significance level alpha and statistical power 1- beta

The industry standard for these two inputs are typically, alpha as 0.05 and power as 0.8.
With these inputs, I’d either use the standard sample size formula for proportions or rely on a calculator tool like Statsmodels in Python.
In practice, a smaller baseline or a smaller MDE means we need a much larger sample to achieve the same confidence.
This ensures the test is neither underpowered (can’t detect real effects) nor overpowered (wasting traffic).

**What is the alpha?**  
The alpha is the significance level, which indicates the probability of type 1 error (the rejected null hypothesis is actually true, false positive in confusion matrix).
  - when alpha is lower, the confidence level of the result is higher and the uncertainty is lower, which means sample size should be larger.

**What is the beta?**  
The beta is the probability of type 2 error (the null hypothesis is failed to reject while the alternative hypothesis is true, false negative in confusion matrix).
  - beta = 1 - power, power is the probability that we want to reject the null hypothesis, common power level is 80%.

**What is the delta?**  
The delta is the minimum detectable effect(MDE), the difference between the control version and the treatment version.
  - the smaller delta wants to detect, the larger the sample size will be needed.

**What is the sigma?**  
The sigma is the standard deviation of the distribution, which indicates how noisy the metric is.
  - the larger sigma means a much bigger sample is needed to detect delta.

**How to design an A/B test about Increase YouTube watch time (end-to-end plan)?**  
I’d run a randomized experiment where users are assigned by user-id to control or personalized autoplay thumbnails. 
Primary metric is average watch time per user over 24 hours. 
I’d compute sample size using baseline variance and a chosen MDE, run the test across at least a weekly cycle, 
use a t-test or bootstrap for inference, monitor guardrail metrics, and apply corrections for multiple tests or interactions before rolling out.

## Evaluating A/B Test  

**What is the p-value?**  
The p-value is the assumed probability that null hypothesis is true.
  a. if the p-value < 0.05, the null hypothesis can be rejected and the result is statistically significant.
  b. if the p-value >= 0.05, there is not enough evidence to reject the null hypothesis.

**What is the test result is not statistically significant?**  
It means there is not enough evidence to say that the treatment group is better than the control group.

**Suppose you run an A/B test and the result is not statistically significant. What would you do next?**  
If a test result isn’t statistically significant, the first step is to check if the test was run long enough and included enough users to reach statistical power, while also accounting for factors like novelty effects or seasonality. Next, I’d review whether we chose the right success metric and if the population is too noisy to hide an effect. 
If everything looks correct, I’d accept that the change may not have a meaningful impact — which is still useful information. 
If there are design issues, I’d adjust — for example by increasing sample size, refining the target users, or clarifying the hypothesis — and then rerun the test.

**What are common pitfalls in A/B Testing?**  
1. Stop the test too early (peeking bias) - follow the predefine sample size and runtime.
2. Underpowered(sample size is too small) - use power analysis to define the effective sample size.
3. Unclear success metric(vague metric to track performance) - preregister primary, secondary and guardrail metrics.
4. Multiple comparisons(too many variants tested at the same time, inflates false positive) - adjust Bonferroni, FDR or clearly label secondary metrics as exploratory.
5. Ignore novelty effect(new design can fade once adapt) - run long enough to see stable behavior, check persistence post-rollout.
6. Poor randomization or contamination(same user sees the both variants or traffic not evenly split) - randomize at stale user_id level.
7. Wrong unit of analysis(randomizing level and analyzing level are different) - align randomization unit with analysis unit.
<img width="953" height="538" alt="ab tesing pitfalls" src="https://github.com/user-attachments/assets/d061231d-181c-407b-afa5-b524e7542cfe" />


**How would you handle multiple A/B tests running at the same time?**  
When multiple A/B tests run at the same time, the main concerns are interaction effects and inflated false positives. 
I’d first check whether the experiments overlap in the user journey — for example, a pricing page test and a checkout flow test may interfere, but a search page test and a recommendation ranking test might not.
If they’re independent, we can safely run them in parallel by splitting traffic randomly. If they target the same users or metrics, I’d consider either staggering them or using a multivariate/factorial design to capture interaction effects.
On the analysis side, I’d apply multiple testing corrections, like Bonferroni or false discovery rate (FDR), to control for inflated Type I error. Finally, I’d ensure traffic is allocated properly so each test remains powered.
