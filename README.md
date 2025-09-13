# Basic A/B Testing Questions  

## Understanding A/B Test  

**What is A/B testing?**  
It's an experimental method used to compare two versions of a product feature to see which one performs better against a defined goal.

**How to explain A/B testing to a non-technical stakeholder?**  
A/B testing is a way to run an experiment where we compare two versions of a product feature. There will be two groups of users, control group and treatment group. 
The control group sees the current version, and the treatment group sees the new version with the change. 
The only difference between the two is the feature we want to test. 
Then we track a key metric — like click-through rate or sign-ups — to see if the new version leads to better results. 
If the difference is big enough, and it’s unlikely caused by chance, we can then confidently decide whether to roll out the new change.

**Why use A/B Testing?**  
1. It helps the company to make data-driven decisions to grow the business and not just rely on guesswork or opinions.
2. It can help the company better understand the users by analyzing how they behave to the certain changes, and from there the user experience could be optimized properly.
   
**What is the framework of A/B Testing?**  
1. Define objective & hypothesis (null + alternative)
2. Select metrics: primary, secondary, guardrails
3. Design variants and allocation (randomization, blocking/stratification)
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

The industry standard for these two inputs are typically, alpha as 0,05 and power as 0.8.
With these inputs, I’d either use the standard sample size formula for proportions or rely on a calculator/tool like Statsmodels in Python.
In practice, a smaller baseline or a smaller MDE means we need a much larger sample to achieve the same confidence.
This ensures the test is neither underpowered (can’t detect real effects) nor overpowered (wasting traffic).

**What is the alpha?**  
The alpha is the significance level, which indicates the probability of type 1 error (the rejected null hypothesis is actually true, false positive in confusion matrix).
  - when alpha is lower, the confidence level of the result is higher and the uncertainty is lower, which means sample size should be larger.

**What is the beta?**  
The beta is the probability of type 2 error (the null hypothesis is failed to rejected while the alternative hypothesis is true, false negative in confusion matrix).
  - beta = 1 - power, power is the probability that we want to reject the null hypothesis, common power level is 80%.

**What is the delta?**  
The delta is the minimum detectable effect(MDE), the gap between the null hypothesis and the alternative hypothesis you care about.
  - the smaller delta wants to detect, the larger the sample size will be needed.

**What is the sigma?**  
The sigma is the standard deviation of the distribution, which indicates how noisy the metric is.
  - the larger sigma means a much bigger sample is needed to detect delta.

**A/B test design: Increase YouTube watch time (end-to-end plan)**  
I’d run a randomized experiment where users are assigned by user-id to control or personalized autoplay thumbnails. 
Primary metric is average watch time per user over 24 hours. 
I’d compute sample size using baseline variance and a chosen MDE, run the test across at least a weekly cycle, 
use a t-test or bootstrap for inference, monitor guardrail metrics, and apply corrections for multiple tests or interactions before rolling out.
