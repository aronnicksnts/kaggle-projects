### PROCESSES DATA FROM \data AND PUTS IT INTO THE DATABASE

from cmath import nan
from unicodedata import category
import sql_commands as sql
import datetime
import uuid
import os
import glob
import pandas as pd

mySQL = sql.SQL()
files = glob.glob(os.path.join(os.getcwd()+"\\data", "*.csv"))

# for file in files:
count = 1
for df in pd.read_csv('D:\\Desktop Folder\\Self Projects\\kaggle-projects\\eCommerce Data Analytics\\data\\2019-Dec.csv', chunksize=1000):
    for index, row in df.iterrows():
        event_time = row['event_time']
        event_type = row['event_type']
        product_id = row['product_id']
        category_code = row['category_code']
        brand = row['brand']
        price = row['price']
        user_id = row['user_id']
        user_session_id = row['user_session']

        #Does event_type exist
        if not mySQL.fromTable_name_exists('event_type', event_type):
            mySQL.add_event_type(event_type)
        #Does brand exist
        if brand and not mySQL.fromTable_name_exists('brand', brand):
            mySQL.add_brand(brand)
        #Does product_id exist
        if not mySQL.fromTable_id_exists('product', product_id):
            if brand:
                brand_id = mySQL.getTable_from_name('brand', brand)[0]
                mySQL.add_product(product_id, price, brand_id)
            else:
                mySQL.add_product(product_id, price)
        #Does category_code exist
        category_parent = 1
        if type(category_code) == str:
            for category_name in mySQL.parse_category(category_code):
                if not mySQL.fromTable_name_exists("category", category_name):
                    mySQL.add_category(category_name, category_parent)
                category_parent = int(mySQL.getTable_from_name('category', category_name)[0])

        if category_parent != 1:
            current_category_id = category_parent

        #Does price exist
        try:
            if price < 0:
                raise ValueError("Price must be higher than 0")
        except Exception as e:
            print(e)
            continue
        #Does user_id exist
        if not mySQL.fromTable_id_exists('user', user_id):
            mySQL.add_user(user_id)
        #Does user_session exist
        if not mySQL.user_session_id_exists(user_session_id):
            mySQL.add_user_session(user_session_id,user_id, event_time)
        #Is user_session_start_time lower than current
        if mySQL.convert_str_datetime(event_time) < mySQL.getTable_user_session(user_session_id)[2]:
            data = {"user_session_start_time": event_time}
            mySQL.modify_user_session(user_session_id, **data)
        #Is user_session_end_time higher than current
        if mySQL.convert_str_datetime(event_time) > mySQL.getTable_user_session(user_session_id)[3]:
            data = {"user_session_end_time": event_time}
            mySQL.modify_user_session(user_session_id, **data)
        
        #INCREMENT PRODUCT_VIEW/ADDED_CART/PURCHASE
        mySQL.product_add_event_type(product_id, event_type)
        #Add the user_activity
        if category_parent != 'ee7c9258-924f-49d3-b4c8-446541f00dc9':
            mySQL.add_user_activity(user_id, event_type, product_id, user_session_id, event_time, current_category_id)
        else:
            mySQL.add_user_activity(user_id, event_type, product_id, user_session_id, event_time)
    print(f"Finished {count*1000}")
    count += 1

