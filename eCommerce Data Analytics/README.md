# Abstract - eCommerce data analytics
This project revolves on finding out the following insights on the following eCommerce's behavioral data in a multi category store to find out:
- how much the eCommerce's sold over the months
- the most/least viewed/purchased
  - Root Node Category
  - Leaf Node Category
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

Additionally, there is extra additional archives that goes from December 2019 - April 2020.

## ERD of the Database
The data from kaggle would be transformed to a MySQL file which has the following tables.
![ECommerce ERD](https://github.com/aronnicksnts/kaggle-projects/blob/main/eCommerce%20Data%20Analytics/ECommerce%20ERD.png)

## Scope and Limits
It is unsure (Will be checked on the future) on if this particular database contains moments where the price of a particular product changes from one point in time to another (Sales). As such, it is assumed that the first encounter of a particular product is its price. The product price is therefore static in this report.

Unfortunately, from one of the discussion in [Kaggle](https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store/discussion/230883), it appears that due to event tracking errors, purchase events from 2019-11-15 and 2020-01-02 is not included.

Additionally, it appears that the brand name of a product may change as stated [here](https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store/discussion/129303), for this study, it will be assumed that one product_id will have a brand, but if the brand name ever changes in any event, that will not be included in the report. This is to increase the speed in preprocessing the database
