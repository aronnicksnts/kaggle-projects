# Abstract - Japan Real Estate Prediction
Three machine learning algorithms were used to predict different Real Estate Purchases all over Japan. 

The data was preprocessed by 
 - removing unnecessary and redundant columns,
 - removing columns where the number of null values in that particular column exceeded 25% of the total dataset,
 - removing rows where they had null values in the remaining columns that were left,
 - checking for correlated values and removing one of the correlated values,
 - conversion of the price to log10 as the dataset was heavily right-skewed,
 - removing of outliers in the dataset,
 - one-hot encoding of categorical values,
 - mean-encoding of categorical values that has many categories,
 - removal of insufficient data and
 - removal of categorical subsets
 
 A total of four models were used for predicting the prices within the dataset. Linear Regression (LR), Multi-Layer Perceptron Regression (MLP), Random Forest Regressor (RF), and Extreme Gradient Boosting Regressor (XGBoost). Among the four models, Random Forest was able to perform the best with a Mean Absolute Percentage Error (MAPE) value of 43%. The four models were able to predict some of the prices within 0.001% off the real price. However, the maximum APE that the four models have gotten is way beyond 2000%. And on most cases, the APE ranges from 0-200%.
 
 It is recommended to check the dataset further and check the representation of low-valued houses as majority of the high APE is caused by houses with a price range from 2 million Yen to 6 million Yen.

## Dataset Link
Download the dataset and extract it to the folder in order to use the code.

[Kaggle Link](https://www.kaggle.com/datasets/nishiodens/japan-real-estate-transaction-prices)

## High APE discussion
![Boxplot APE](https://github.com/aronnicksnts/kaggle-projects/blob/main/Japan%20Real%20Estate%20Prediction/Images/BoxplotAPE.png)

The image above shows the boxplot of the average percentage error (APE) of the four models. There are a lot of outliers which goes beyond 100%. LR had the worst performance amongst the four models with the maximum APE above 3500%.

![Histogram APE RF](https://github.com/aronnicksnts/kaggle-projects/blob/main/Japan%20Real%20Estate%20Prediction/Images/HistogramAPERF.png)

A histogram of the APE is made for all of the models, the figure above in particular showcases the APE of the best performing model, RF. From here, it can be seen that majority of the error rate ranges from 0-100%, but there are some outliers which can go to as high as 2361%.

### Sample values of Random Forest Predictions with high APE

| Actual    | RF Prediction | RF APE (%) |
|-----------|---------------|------------|
| 3,000,000 | 24,689,511.85 | 723        |
| 5,700,000 | 24,602,724.41 | 332        |
| 3,000,000 | 18,514,732.23 | 517        |
| 2,500,000 | 13,060,899.43 | 422        |
| 4,300,000 | 31,259,693.27 | 627        |

Checking the real values and predicted values of values with high APE, the actual value can be seen to be around only 2.5 million to 5.7 million Yen, whilst the predicted value can go over 10 million Yen, producing a very high APE. Other models have a similar problem, where-in the actual value ranges on the lower end of the dataset, whilst the prediction of the model is a much higher number compared to the actual value. This could be due to the lack of representation of the low valued houses. Further checking of these data is recommended.
