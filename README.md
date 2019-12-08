## Low likelihood of returning to normal weight after weight gain

_Seth Rhoades_

### Introduction

Population health trends are typically observed through cross-sectional analysis. While this analysis is useful from a macroscopic perspective, it cannot capture the granularity of an individual's health across time. For example, rates of obesity have risen in the past decades. However, at the level of individuals, how likely is it that someone can return to normal weight, once that person enters an obese state? Or framed as a Markov Chain, is obesity an absorbing state, where an individual cannot return to normal weight? The distinction between individual health states over the time dimension, and population level cross-sectional observations, is helpful to clarify how one can improve the human condition. If the reversibility of obesity is likely, then the rise of obesity may be more attributable to insufficient or inaccessible treatment for those who remain obese. If reversbility of obesity is unlikely, then the rise of obesity may be more attributable to ineffective treatments.

This work analyzes the National Longitudinal Survery of Youth, which is a sample of approximately 9000 adolescents that began in 1997. Body mass index (BMI) was calculated for individuals who particpated across multiple years, followed by the frequencies of individuals in strata of underweight, normal, overweight, or obese from one year to the next. These findings demonstrate that upon entering an overweight or obese state after adolescence, the likelihood of transitioning back to a normal weight is unfavorable, particularly in males.


### Methods

#### Data sources

The National Longitudinal Survey of Youth 1997 (NLSY97) is part of the National Longitudinal Surveys (NLS) program. This particular cohort consists of individuals born between 1980 and 1984, and consist of 51% males, 49% females with diverse backgrounds (52% Non-black/Non-Hispanic, 26% Black Non-Hispanic, and 21% Hispanic). At the time of first interview, respondents' ages ranged from 12 to 18. The respondents were 30 to 36 at the time of their round 17 interviews in 2015-2016. Data was accessed from the NLS Investigator portal (https://www.nlsinfo.org/investigator). 

To categorize BMI as underweight, normal, overweight, or obese in non-adults, BMI-for-age charts were accessed from the Centers of Disease Control and Prevention (CDC) (https://www.cdc.gov/growthcharts/percentile_data_files.htm). 

#### Weight strata transition counting

BMI was calculated for each individual in the NLYS97 cohort (weight/height^2). For ages less than 20 years, BMI percentiles were taken from the CDC's BMI-for-age charts. Underweight BMI was categorized as less than then 5th percentile for non-adults and less than 18.5 BMI for adults. Normal weight BMI was categorized as between the 5th and 85th percentiles for non-adults and between 18.5 and 25 for adults. Overweight BMI was categorized as between the 85th and 95th percentiles for non-adults and between 25 and 30 for adults. Obese BMI was categorized as above the 95th percentile for non-adults and above 30 for adults.

After extracting BMI for each individual's life-year, counts were enumerated for each one-to-any transition of weight strata (e.g. number of normal weight individuals at age 13 who enter an underweight, normal, overweight, or obese state at age 14). These counts were then normalized by the total individuals in that life year, by gender. 


### Results

Conditional on weight strata, for both males and females, the transitions between normal and overweight, and overweight and obese were largely favorable during adolescence (Figures 1 and 2). For instance, at age 15, 5% of normal weight females transitioned to overweight status at age 16, while 32.1% of overweight females transitioned to normal weight (7.5% and 31.1% for males, respectively). 17.1% of overweight females transitioned to obese, compared to 21% from obese to overweight (16.9% and 18.8% for males, respectively). 92.6% of females remain normal weight, 50.7% remain overweight, and 42.8% remain obese (90.8%, 51.9%, and 77.1% respectively in males). At age 25, the difference in transition rates decreased. 11.2% of normal weight females transitioned to overweight at age 26, while 20% of overweight females transitioned to normal weight (13.5% and 9.1% for males, respectively). 17% of overweight females transitioned to obese, compared to 8.4% from obese to overweight (10% and 13% in males, respectively).

When normalized across all possible state transitions, the transitions between normal and overweight, and overweight and obese, were largely neutralized during adolescence (Figures 3 and 4). 3.9% of all females at age 15 transitioned from normal weight to overweight, and 3.9% transitioned from overweight to normal at age 16 (5.2% and 5% for males, respectively). 2.1% of females transitioned from overweight to obese, and 1.5% transitioned from obese to overweight (2.7% and 2.4% for males, respectively). 5.5% of all females at age 25 transitioned from normal weight to overweight, and 4.9% transitioned from overweight to normal at age 26 (5% and 3.6% for males, respectively). 4.2% transitioned from overweight to obese, and 1.9% transitioned from obese to overweight (3.9% and 3% for males, respectively).

In conclusion, the transition probabilties between weight strata is more evenly distributed during adolescence. However, by adulthood, these states are more absorbing, where overweight or obsese individuals are more likely to maintain their weight status. In general, these probabilities are less favorable for males than females. Importantly, when analyzing health trajectories on an individual basis, ergodicity should not be assumed. Weight maintenance, and the proper education and intervention (when truly necessary) should be stressed during adolescence, as the challenge of altering weight in adulthood is generally greater. Importantly, these unfavorable transition rates shed light on a need for more effective interventions.


#### References

Bureau of Labor Statistics, U.S. Department of Labor. National Longitudinal Survey of Youth 1997 cohort, 1997-2013 (rounds 1-16). Produced by the National Opinion Research Center, the University of Chicago and distributed by the Center for Human Resource Research, The Ohio State University. Columbus, OH: 2015.
