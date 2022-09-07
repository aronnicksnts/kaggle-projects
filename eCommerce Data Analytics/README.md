# Abstract - eCommerce data analytics
This project revolves on finding out the following insights on the following eCommerce's behavioral data in a multi category store to find out:
- how much the eCommerce's sold over the months
- the most/least viewed/purchased category
- most popular item per month
- most popular item per specific event (Christmas, Halloween, New Year's, etc.)
- most purchased item
- least purchased item
- which item has the most revenue
- the most wanted item
- product price distribution
- product purchase distribution per month/in a whole

## Dataset Link
Download the dataset and extract it to a folder named 'data' in order to use the code.

[Kaggle Link](https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store?select=2019-Oct.csv)

Additionally, there is extra additional archives that goes from October 2019 - April 2020.

## ERD of the Database
The data from kaggle would be transformed to a MySQL file which has the following tables.
![ECommerce DataWarehouse](https://github.com/aronnicksnts/kaggle-projects/blob/main/eCommerce%20Data%20Analytics/ECommerce%20ERD.png)


## Scope and Limits
Unfortunately, from one of the discussion in [Kaggle](https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store/discussion/230883), it appears that due to event tracking errors, purchase events from 2019-11-15 and 2020-01-02 is not included.

This project would not be able to determine individual user activities as the data events are aggregated to a summary of a whole day.
