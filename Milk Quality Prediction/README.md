# Abstract - Milk Quality Prediction
With different qualities of milk from the dataset which contains *high*, *medium*, and *low* quality milk differentiating from their pH levels, temprature, taste, odor, fat, turbidity, and colour, the following report tries and aims to predict the milk's quality based on the dataset. 

A linear regression model was used to try and predict the milk's quality. Based from the results, the model was able to get an overall f1-score of 70%. Based from the confusion matrix, the model had the most inaccuracy when it tries to differentiate between a high quality milk and a low quality milk when the milk's quality is a high grade with about 42% precision. However, when the milk's quality is low grade, the model had almost no trouble in correctly predicting that it was a low grade model. With about 80% precision. The model was most accurate in predicting the milk's quality when it is medium with a 78% f1-score and 72% precision.


## Dataset Link
Download the dataset and extract it to the folder in order to use the code.

[Kaggle Link](https://www.kaggle.com/datasets/cpluzshrijayan/milkquality)