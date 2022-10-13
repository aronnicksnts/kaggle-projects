# What it is about
Applying various methods to different kaggle projects. Mostly machine learning and data analytics.


### Table of Contents
- [Lemon Quality](#lemon-quality)
- [Flower Recognition](#flower-recognition)
- [Fortune Top 1000 Companies by Revenue 2022](#fortune-top-1000-companies-by-revenue-2022)
- [Lung Disease Classification](#lung-disease-classification)
- [Milk Quality Prediction](#milk-quality-prediction)

## Lemon Quality

The project aims to predict the quality of a lemon based on the image. There are three classifications of the lemon, a good quality lemon, a bad quality lemon, and an empty background. The AlexNet CNN architecture was used for the model. The model's hyperparameters were as follows: 10 epochs, 128 batch_size and 5-fold cross validation with 70% being the testing set and 30% being the test set. The model was able to achieve an accuracy of 99% with validation loss of 0.05

## Flower Recognition

Utilizes the knn algorithm and cnn to try and predict what type of flower is in the photo. With the knn algorithm, the model was able to get an accuracy of 35%. The cnn had a total of 10 epochs and was able to perform better compared to the knn algorithm, with an accuracy of 62%.

## Fortune Top 1000 Companies by Revenue 2022

An analysis of the Fortune 1000 companies comparing their profit, margins, market value, and revenue to each other. From the analysis, it appears that the top 10 companies usually have majority of the percentages in terms of profit, market value, and revenue. 

## Lung Disease Classification

With the usage of a CNN algorithm, the model was able to get an overall 95% accuracy in terms of predicting whether the patient either has COPD, URTI, Bronchiectasis, Pneumonia, Bronchiolitis, or none of the above (meaning they are healthy). The model had the most confusion on predicting whether the patient has either COPD or pnuemonia. It is also recommended to have a more diverse dataset as most of the data are patient with COPD.

## Milk Quality Prediction

With a lienar regression model, the aim of the project was to predict what grade the milk had based on its different characteristics. There are 3 different grades, high, medium, and low. There is also a total of 7 different characteristics that the milk had. Comparing the characteristics of the grades to each other, it was found out that the characteristic 'taste' would have no bearing to what grade of milk it was, it was then dropped before the model was ran. The linear regression model had an accuracy of 70%
