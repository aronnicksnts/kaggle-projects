### PROCESSES DATA FROM \data AND PUTS IT INTO THE DATABASE

from cmath import nan
from unicodedata import category
import sql_commands as sql
import datetime
import os
import glob
import pandas as pd

mySQL = sql.SQL()
files = glob.glob(os.path.join(os.getcwd()+"\\data", "*.csv"))

# for file in files:
count = 1
#Initialization of lists
product_dict = {} #Contains dictionaries in which it has product_price, brand_id, and next_product_id
date_dict = {}
check = 1

print(mySQL.getProductTable(1))

# for df in pd.read_csv('D:\\Desktop Folder\\Self Projects\\kaggle-projects\\eCommerce Data Analytics\\data\\2019-Oct.csv', chunksize=15000):
#     for index, row in df.iterrows():
#         pass


