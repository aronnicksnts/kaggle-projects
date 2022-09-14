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
product_dict = {}
currentDate = None


for df in pd.read_csv('D:\\Desktop Folder\\Self Projects\\kaggle-projects\\eCommerce Data Analytics\\data\\2019-Oct.csv', chunksize=15000):
    df = df.fillna("")
    for index, row in df.iterrows():

        #Check Date is current date and if not, refresh product_dict
        currDate = datetime.datetime.strptime(str(row['event_time'][:-4]), '%Y-%m-%d %H:%M:%S').date()
        if currDate != currentDate:
            if not mySQL.checkDateExists(currDate):
                mySQL.createNewDate(currDate)
            currentDate = currDate
            dateKey = mySQL.getDateKey(currentDate)
            product_dict = {}
        
        #Check product_id in product_dict
        if not row['product_id'] in product_dict:
            if not mySQL.checkProductExists(row['product_id']):
                mySQL.createNewProduct(row['product_id'], row['category_id'], row['price'], row['category_code'], row['brand'])
            #Compare current product
            productInfo = mySQL.getProductTable(row['product_id'])
            productKey = productInfo[0]
            if productInfo[3] == None:
                categoryCode = ''
            else:
                categoryCode = productInfo[3]
            if productInfo[5] == None:
                brand = ''
            else:
                brand = productInfo[5]
            if productInfo[2] != row['category_id'] or categoryCode != row['category_code'] or productInfo[4] != row['price'] \
                or brand != row['brand']:
                mySQL.disableProduct(productInfo[0])
                mySQL.createNewProduct(row['product_id'], row['category_id'], row['price'], row['category_code'], row['brand'])
                productInfo = mySQL.getProductTable(row['product_id'])
                productKey = productInfo[0]

            product_dict[row['product_id']] = productKey

            #Create new Fact Product
            mySQL.createFactProduct(productKey, dateKey, row['event_type'])
        
        else:
            mySQL.incrementFactProduct(product_dict[row['product_id']], dateKey, row['event_type'])

    print(f"Processed {count*15000}")
    count += 1


