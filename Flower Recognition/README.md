# Abstract - Flower Recognition
With a dataset of 4242 images of flowers, this project utilizes the knn algorithm in order to predict if the flower is either a **daisy**, **dandelion**, **rose**, **sunflower**, or a **tulip**. With the knn algorithm, the model was 35% accurate, it also appears that the model has created a bias towards the label daisy. However, with the cnn algorithm after 10 epochs, it was able to have an accuracy of 62%. In comparing the two, we can conclude that the convolutional neural network algorithm is better compared to k-nearest neighbor algorithm.
## Dataset Link
Download the dataset and extract it to the folder in order to use the code.

[Kaggle Link](https://www.kaggle.com/datasets/alxmamaev/flowers-recognition)

## Dataset Samples

![Dataset Amt](https://github.com/aronnicksnts/kaggle-projects/blob/main/Flower%20Recognition/dataset_amt.png)

## CNN Results
![CNN Confusion Matrix](https://github.com/aronnicksnts/kaggle-projects/blob/main/Flower%20Recognition/cnn_confusion_matrix.png)

With 256 as the batch size and 10 epochs, the model was able to achieve 62% overall accuracy in predicting what type of flower the image had.

The model had difficulty in assessing whether the sample was either daisy or dandelion with the model being incorrect 30% of the time when it was actually daisy but instead the model predicted that it was a dandelion. With the dandelion's case, it was mostly accurate with it being able to correctly predict at 79% of the time. With the rose's case, it was mostly purely guessing with about 37% accuracy on getting it correct that it was a rose. It incorrectly identified it as either a daisy, a tulip, or a dandelion with 21%, 20%, and 15% respectively. With the sunflower's case, it was mostly accuracy having 80% accuracy. Finally, with the tulip, it was approximately 50% accuracte, confusing it to the other flowers almost evenly at around 9-14%. 


## KNN Results

![KNN Confusion Matrix](https://github.com/aronnicksnts/kaggle-projects/blob/main/Flower%20Recognition/knn_confusion_matrix.png)

In the case of the K-nearest neighbor's algorithm, it appears that the model was only 35% accurate overall, it appears that the model tried to predict that the image's label was daisy in most of the cases that it incorrectly predicted the flower type. With this approach, the model was able to have an 80% accuracy on assessing whether the flower was a daisy or not. However, the dandelion, rose, sunflower, and tulip received an accuracy of 20%, 22%, 37%, and 23% respectively. Having their recall score incredibly low at 20%, 22%, 38%, and 23%. With this, we can say that the model created a bias towards the label daisy in which it mostly predicted that the flower was a daisy 703 of the 1080 test cases
