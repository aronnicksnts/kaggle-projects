# Abstract - Japan Real Estate Prediction
Three machine learning algorithms were used to predict different Real Estate Purchases all over Japan. 

The data was preprocessed by 
 - removing unnecessary and redundant columns,
 - removing columns where the number of null values in that particular column exceeded 25% of the total dataset,
 - removing rows where they had null values in the remaining columns that were left,
 - checking for correlated values and removing one of the correlated values,
 - conversion of the price to log2 as the dataset was heavily right-skewed,
 - removing of outliers in the dataset,
 - one-hot encoding of categorical values,
 - mean-encoding of categorical values that has many categories,
 - removal of insufficient data and
 - removal of categorical subsets
 
 The model used for the dataset were linear regression, multi-layer perceptron regressor (MLPRegressor), and XGBoost. Among the three models, the XGBoost was able to perform most accurately with an average MAPE score of 63%, whilst the linear regression and MLPRegressor got an average MAPE score of 81% and 68% respectively.

## Dataset Link
Download the dataset and extract it to the folder in order to use the code.

[Kaggle Link](https://www.kaggle.com/datasets/nishiodens/japan-real-estate-transaction-prices)
