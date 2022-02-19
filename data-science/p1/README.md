#Analyzing the NYC Subway Dataset
by Allan Reyes in fulfillment of Udacity’s Data Analyst Nanodegree, Project 1
##Section 1. Statistical Test
*1.1 Which statistical test did you use to analyse the NYC subway data? Did you use a one-tail or a two-tail P value? What is the null hypothesis? What is your p-critical value?*

> I used the Mann-Whitney U test to analyze the NYC subway data.  Because it is not yet known, nor hypothesized, which data set would be higher or lower, a two-tailed test here is apt. In using the Mann-Whitney U test, the null hypothesis is that the two populations are the same, or simply put, that rain has no correlation with ridership.  The p-critical value used was 0.05, or 5%.

*1.2 Why is this statistical test applicable to the dataset? In particular, consider the assumptions that the test is making about the distribution of ridership in the two samples.*

> As shown in Section 3.1, neither the rain or no-rain histograms are normally-distributed.  As such, a non-parametric test such as Mann-Whitney U is a good fit, while a test such as Welch’s two-sample t-test is not.  To quantitatively capture and confirm that neither data sets are normally-distributed, a Shapiro-Wilk test could have been conducted.

*1.3 What results did you get from this statistical test? These should include the following numerical values: p-values, as well as the means for each of the two samples under test.*
> ```
Mean entries with rain: 1105.446
Mean entries without rain: 1090.279
U-statistic: 1924409167.0
p-value: 0.025
```

*1.4 What is the significance and interpretation of these results?*

> Comparing the means yields 1.4% more subway entries when it rains.  This statistic alone is insufficient in drawing conclusions or correlation.  The U-statistic has a high value, very close to the maximum value of 1937202044.0, or half the product of the number of values in each data set.  A U-statistic of half the maximum would indicate that the null hypothesis is true.  Of note, the p-value 0.025 satisfies the p-critical value, and the conclusion can be drawn with 95% confidence that the null hypothesis is false and that ridership is different with vs. without rain.

##Section 2. Linear Regression
*2.1 What approach did you use to compute the coefficients theta and produce prediction for ENTRIESn_hourly in your regression model?*

> A machine learning algorithm, batch gradient descent, was used to train the linear regression coefficients.  I used the default values of learning rate (alpha) 0.1 and 75 iterations, and also kept the mean normalization feature scaling.  The given values were sufficient in converging on a local minimum, as confirmed by plotting the cost history vs. number of iterations.

*2.2 What features (input variables) did you use in your model? Did you use any dummy variables as part of your features?*

> Features used included rain (0 or 1), precipitation, mean wind speed, hour, and mean temperature.  Per the default configuration, dummy variables were introduced for features ‘UNIT’ (the turnstile location/identification number), which were categorical in nature.  They were initialized with boolean (0 or 1) features with prefix ‘unit,’ and each data point would have a ‘1’ in the feature that it “belonged” to.  It did not make sense to apply linear regression to the raw ‘UNIT’ parameters quantitatively; however, it was important to keep track of it as there was a wide variation between different subway stops and account for it first.  If this was not done, the differences between different turnstiles would mask the markedly smaller changes due to rain, precipitation, hour, or temperature.

*2.3 Why did you select these features in your model? We are looking for specific reasons that lead you to believe that the selected features will contribute to the predictive power of your model.*

> I maintained rain, precipitation, hour, and mean temperature because out of experimentation, I was unable to find R^2 values that were better.  Broadening the hypothesis that “people use the subway more often when it’s raining” to “people use the subway more often when there’s bad weather outside,” I also included wind speed.  I saw a slight increase in my R^2 values. 

*2.4 What are the coefficients (or weights) of the non-dummy features in your linear regression model?*

> `[-4.24736210e+00, 8.60518981e+00, 4.64832083e+01, 4.64163466e+02, -3.19114921e+01, 1.08898857e+02]`

*2.5 What is your model’s R2 (coefficients of determination) value?*

> `0.458375428174`

*2.6 What does this R2 value mean for the goodness of fit for your regression model? Do you think this linear model to predict ridership is appropriate for this dataset, given this R2 value?*

> R^2 is essentially the percentage of variance that is explained, and is a quantitative measure of the “goodness of fit.”  While it only explains 45.8% of variation, I think a better metric is to plot the residuals.

![Residuals histogram](https://raw.githubusercontent.com/allanbreyes/udacity-data-science/master/p1/figures/residuals-histogram.png)

> To decisively conclude whether or not this model was a good fit certainly depends on the context and use case for the prediction data.  If this were a use case that had safety and security concerns, it would certainly be insufficient!  The residual plot shows that most of the residuals were close to `0 +/- 5,000`.  Qualitatively, and for the objective of being able to “ballpark” ridership, the linear model is sufficient.

> Further and advanced study could include more features or utilize polynomial regressions.  However, this might lead to significant over-fitting, and the model may fail on new data sets.  In that case, regularization would be a good method to attenuate any over-fitting.

##Section 3. Visualization
*3.1 Include and describe a visualization containing two histograms: one of  ENTRIESn_hourly for rainy days and one of ENTRIESn_hourly for non-rainy days.*

![ENTRIESn_hourly histogram](https://raw.githubusercontent.com/allanbreyes/udacity-data-science/master/p1/figures/histogram-of-ENTRIESn_hourly-rain-vs-no-rain.png)

> Plotting overlaid histograms of subway entries for both rainy and dry hours shows that both distributions are not normally-distributed.  Of note, it’s important to clarify that these are aggregate values and that there were less rainy days than there were not rainy days; it would be grossly incorrect to draw from this graph that subway ridership is less when it rains. 

*3.2 Include and describe a freeform visualization.*

![Average subway entries by time of day](https://raw.githubusercontent.com/allanbreyes/udacity-data-science/master/p1/figures/average-subway-entries-by-time-of-day.png)

> By plotting the average number of subway entries at each hour, it’s clear that there are several peaks throughout the day, with the most prominent ones being at noon and 8pm.  Interestingly, these peaks are larger than those during rush hours (8-9am and 5-6pm).  It raises some intriguing questions about the demographics and characteristics of NYC subway riders: assuming a 9-5pm workday, why are more subway entries occurring at 5pm vs. 9am? Are more people going out to lunch (12pm) and dinner (8pm), or is that there work schedule?  Without any demographic data, it would be impossible to determine these questions from the current data set.

##Section 4. Conclusion
*4.1 From your analysis and interpretation of the data, do more people ride the NYC subway when it is raining or when it is not raining?*

> Particularly given the results from the Mann-Whitney U test (p-value: 0.025), we can say with a high level of certainty that more people ride the NYC subway when it is raining.  It is important to note that simply looking at the means of both data sets is insufficient, due to variance.  The Mann-Whitney U test is needed to quantitatively confirm that the two data sets are statistically different.

*4.2 What analyses lead you to this conclusion? You should use results from both your statistical tests and your linear regression to support your analysis.*

> The positive coefficient for the rain (0 or 1) parameter indicates that the presence of rain contributes to increased ridership.  This may have not been the case for all data points, with the R^2 being approximately 46%; however, the small residuals show relatively high accuracy, given our objectives.  Although the means of both data sets are not that different from each other, the Mann-Whitney U test did indicate that there was a statistically significant change in ridership for rain vs. no-rain.  It is conscientious to claim that rain increases subway ridership.

##Section 5. Reflection
*5.1 Please discuss potential shortcomings of the methods of your analysis, including: data set, linear regression model, and statistical tests.*

> One immediate red flag that was presented while exploring the data was that there were markedly more entries than there were exits.  The only logical explanations could be that there were miscounts, or some turnstiles/stations were not included in the data set.  Presumably, this would have had an equivalent effect on both rain and no-rain data sets, so for the purposes of this study, it likely had little to no effect.

> A combination of increased sample size (larger data set) and normalization by location/turnstile ID could have potentially increased the confidence of both the Mann-Whitney U test and the linear regression model.  As we saw from examining the ‘UNIT’ column, ridership varied greatly.  Simply put, some stations and turnstiles were naturally more active than others.  The Mann-Whitney U test did not take this into account, and only looked at the subway entry distributions for rain and no-rain.  Examining how the same stations at the same day and time varied by rain could have increased the fidelity of the test.

> The linear regression model was adequate for the purpose of the study, but could certainly have been improved.  It’s possible that the region of study had a linear relationship, but it is still an assumption and simplification.  Considering the extreme, subway ridership certainly has an asymptotic limit; only so many riders can get on the subways!  As mentioned in Section 2.6, the inclusion of more features or polynomial combinations could have increased the accuracy of the model.  Given more data, it would have also been appropriate to split the data into a training data set (~60%), a cross-validation data set (~20%), and a testing set (~20%).  This could have illuminated any errors with high variance, high bias, and any over/under-fitting.

*5.2 Do you have any other insight about the dataset that you would like to share with us?*

> I think that an interesting investigation would be to use gradient descent with logistic regression to see if one might be able to predict if it rained or not given various parameters, to include turnstile location/ID, time of day, and subway entries.  Intuitively, this might produce false positives or negatives on special days (e.g. sports game, holidays, etc.).

##References
- [Stanford Machine Learning Class](https://www.coursera.org/course/ml)
- [SciPy Documentation](http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html#scipy.stats.mannwhitneyu)
- [Mann-Whitney U Test Wiki](http://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test)
- [GraphPad](http://www.graphpad.com/guides/prism/6/statistics/index.htm?how_the_mann-whitney_test_works.htm)
- [Piazza posts](https://piazza.com/class/i2ddoj5wy8i6j5?cid=17)