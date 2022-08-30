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
#Initialization of lists
brand_dict = {}
product_dict = {} #Contains dictionaries in which it has product_price, brand_id, and next_product_id
user_session_dict = {} #Contains a hashmap with user_session_id as the key and has values of the end_time and start_time
product_event_list = [] #List of dictionaries which has product_id, event_type and user_id
user_activity_category_list = []
user_activity_nocategory_list = []
category_list = []

for df in pd.read_csv('D:\\Desktop Folder\\Self Projects\\kaggle-projects\\eCommerce Data Analytics\\data\\2019-Oct.csv', chunksize=10000):
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
        # if not mySQL.fromTable_name_exists('event_type', event_type):
        #     mySQL.add_event_type(event_type)

        #Is brand in dictionary add if not so
        
        if type(brand) == str and brand not in brand_dict:
            if brand and not mySQL.fromTable_name_exists('brand', brand):
                mySQL.add_brand(brand)

            brand_data = mySQL.getTable_from_name('brand', brand)
            brand_dict[brand_data[1]] = brand_data[0]
        #Does product_id exist in dictionary add if not so
        if product_id not in product_dict:
            if not mySQL.fromTable_id_exists('product', product_id):
                if type(brand) == str:
                    brand_id = mySQL.getTable_from_name('brand', brand)[0]
                    mySQL.add_product(product_id, price, brand_id)
                    product_dict[product_id] = {"product_price": price,
                    "brand": brand_dict[brand]}
                    continue
                else:
                    mySQL.add_product(product_id, price)
            product_data = mySQL.getTable_from_id('product', product_id)
            if type(brand) == str:
                product_dict[product_id] = {"product_price": price,
                "brand": brand_dict[brand]}
                continue
            product_dict[product_id] = {"product_price": price}
            
        #Does category_code exist
        category_parent = 1
        if type(category_code) == str:
            for category_name in mySQL.parse_category(category_code):
                if category_name in category_list:
                    continue
                if not mySQL.fromTable_name_exists("category", category_name):
                    mySQL.add_category(category_name, category_parent)
                category_parent = int(mySQL.getTable_from_name('category', category_name)[0])
                category_list.append(category_name)

        if category_parent != 1:
            current_category_id = category_parent

        #Does price exist
        try:
            if price < 0:
                raise ValueError("Price must be higher than 0")
        except Exception as e:
            print(e)
            continue
        #Does user_id exist if not, add user
        mySQL.add_user(user_id)
        
        
        if user_session_id not in user_session_dict:
            #Does user_session exist
            if not mySQL.user_session_id_exists(user_session_id):
                mySQL.add_user_session(user_session_id,user_id, event_time)
            current_user_session = mySQL.getTable_user_session(user_session_id)
            user_session_dict[user_session_id] = {"user_session_start_time": current_user_session[2],
                                                "user_session_end_time": current_user_session[3]}
        #Is user_session_start_time lower than current
        if type(user_session_dict[user_session_id]["user_session_start_time"]) != datetime.datetime:
            user_session_dict[user_session_id]["user_session_start_time"] = mySQL.convert_str_datetime(
                user_session_dict[user_session_id]["user_session_start_time"])
        if mySQL.convert_str_datetime(event_time) < user_session_dict[user_session_id]["user_session_start_time"]:
            user_session_dict[user_session_id]["user_session_start_time"] = event_time
            data = {"user_session_start_time": event_time}
            mySQL.modify_user_session(user_session_id, **data)
        #Is user_session_end_time higher than current
        if type(user_session_dict[user_session_id]["user_session_end_time"]) != datetime.datetime:
            user_session_dict[user_session_id]["user_session_end_time"] = mySQL.convert_str_datetime(
                user_session_dict[user_session_id]["user_session_end_time"])
        if mySQL.convert_str_datetime(event_time) > user_session_dict[user_session_id]["user_session_end_time"]:
            user_session_dict[user_session_id]["user_session_end_time"] = event_time
            data = {"user_session_end_time": event_time}
            mySQL.modify_user_session(user_session_id, **data)

        
        #INCREMENT PRODUCT_VIEW/ADDED_CART/PURCHASE
        product_event = {"product_id": product_id, "event_type": event_type, "user_id": user_id, 'price': price}
        product_event_list.append(product_event)
        #Add the user_activity to list
        if category_parent != 1:
            user_activity = {"user_id": user_id, "event_type": event_type, "product_id": product_id,
                            "user_session_id": user_session_id, "event_time": event_time,
                            "category_id": current_category_id}
            user_activity_category_list.append(user_activity)
        else:
            user_activity = {"user_id": user_id, "event_type": event_type, "product_id": product_id,
                            "user_session_id": user_session_id, "event_time": event_time,
                            }
            user_activity_nocategory_list.append(user_activity)
    print(f"Processed {count*10000}")
    count += 1
    if len(product_event_list) > 50000:
        mySQL.batch_product_event(product_event_list)
        product_event_list = []
        print(f"Added {len(product_event_list)} product_events to the database")
    if len(user_activity_category_list)+len(user_activity_nocategory_list) > 50000:
        mySQL.batch_user_activity_cat(user_activity_category_list)
        mySQL.batch_user_activity_nocat(user_activity_nocategory_list)
        user_activity_category_list = []
        user_activity_nocategory_list = []
        print(f"Added {len(user_activity_category_list)+len(user_activity_nocategory_list)} user_activity to the database")
        
    if count % 35 == 0:
        brand_dict = {}
        product_dict = {} #Contains dictionaries in which it has product_price, brand_id, and next_product_id
        user_session_dict = {} #Contains a hashmap with user_session_id as the key and has values of the end_time and start_time
        category_list = []

mySQL.batch_product_event(product_event_list)
print(f"Added remaining {len(product_event_list)} product events to the database")
mySQL.batch_user_activity_cat(user_activity_category_list)
mySQL.batch_user_activity_nocat(user_activity_nocategory_list)
print(f"Added remaining {len(user_activity_category_list)+len(user_activity_nocategory_list)} user activity to the database")
