# Abstract - Lemon Quality Dataset
This project tries and predict the quality of an image of a lemon, whether it is a good quality lemon or a bad quality lemon. There are also images where-in no lemon was shown and only the background is visible in the image. The Alexnet CNN architecture was used for the model. The model had the hyperparameters as 10 epochs, 128 batch_size and k-fold equal to 5. A total of 2528 images was used for the dataset. 70% of the data was used for the training of the model and 30% was for testing the model. 

## Dataset Link
Download the dataset and extract it to the folder in order to use the code.

[Kaggle Link](https://www.kaggle.com/datasets/yusufemir/lemon-quality-dataset)

## Confusion Matrix of Model

![Confusion_Matrix_Lemon](https://github.com/aronnicksnts/kaggle-projects/blob/main/Lemon%20Quality%20Dataset/Confusion_Matrix_HeatMap.jpg)

From the image above, it can be seen that the model was able to get good results where it was able to detect if there was no lemon in the image, and was able to get an overall f1 score of 99%, only having the wrong prediction in a total of 8 images out of 759 images in the test set. The model was mostly wrong when differentiating between a bad quality lemon, predicting that it was a good quality lemon.
