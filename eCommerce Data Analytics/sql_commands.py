from datetime import datetime
from itertools import product
from multiprocessing.sharedctypes import Value
from sqlite3 import connect
from tokenize import Double
from unicodedata import category
import mysql.connector
from mysql.connector import Error
import json
import uuid
import datetime

class SQL:

    def __init__(self):
        try:
            mysqlData = json.load(open('sql_data.json'))
            self.conn = mysql.connector.connect(host=mysqlData['host'],
                                                    database=mysqlData['database'],
                                                    user=mysqlData['user'],
                                                    password=mysqlData['password'])

            if self.conn.is_connected():
                    db_Info = self.conn.get_server_info()
                    print("Connected to MySQL Server version ", db_Info)
                    self.cursor = self.conn.cursor()
        except Error as e:
            print("Error while connecting to MySQL", e)
        
    def disconnect(self):
        try:
            self.cursor.close()
            self.conn.close()
            print("Successfully disconnected to the database")
        except Error as e:
            print("Error: ", e)

    @staticmethod
    def generate_random_number():
        return int(uuid.uuid4())


    @staticmethod
    def generate_random_id():
        return str(uuid.uuid4())


    @staticmethod
    def combine_query(table_name, id, data):
        query = f"UPDATE {table_name} SET "
        for (key, value) in data.items():
            if type(value) == int:
                query += f"{key} = {value}, "
            else:
                query += f"{key} = '{value}', "
        query = query[:-2] + f" WHERE {table_name}_id = {id}"
        return query

    @staticmethod
    def combine_query_strid(table_name, id, data):
        query = f"UPDATE {table_name} SET "
        for (key, value) in data.items():
            if type(value) == int:
                query += f"{key} = {value}, "
            else:
                query += f"{key} = '{value}', "
        query = query[:-2] + f" WHERE {table_name}_id = '{id}'"
        return query


    def fromTable_remove_id(self, table_name, id):
        try:
            if not self.fromTable_id_exists(table_name, id):
                raise NameError(f"{table_name}_id {id} does not exist in the database")
            
            query = f"UPDATE {table_name} SET '{table_name}_active' = 0 WHERE {table_name}_id = {id}"
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)


    def fromTable_name_exists(self, table_name, name) -> bool:
        try:
            query = f"SELECT EXISTS (SELECT * FROM {table_name} WHERE {table_name}_name = '{name}')"
            self.cursor.execute(query)
            if self.cursor.fetchone()[0] == 0:
                return False
            return True
            

        except Exception as e:
            print(e)
    

    def fromTable_id_exists(self, table_name, id) -> bool:
        query = f"SELECT EXISTS (SELECT * FROM {table_name} WHERE {table_name}_id = {id})"
        self.cursor.execute(query)
        if self.cursor.fetchone()[0] == 0:
            return False
        return True


    def getTable_from_id(self, table_name, id):
        try:
            query = f"SELECT * FROM {table_name} WHERE {table_name}_id = {id}"
            self.cursor.execute(query)
            table = self.cursor.fetchone()
            if table is None:
                return tuple()
            return table
        except Exception as e:
            print(e)
    

    def getTable_from_name(self, table_name, name):
        try:
            query = f"SELECT * FROM {table_name} WHERE {table_name}_name = '{name}'"
            self.cursor.execute(query)
            table = self.cursor.fetchone()
            if table is None:
                return tuple()
            return table
        except Exception as e:
            print(e)

    def getId_from_name(self, table_name, name):
        try:
            query = f"SELECT {table_name}_id FROM {table_name} WHERE {table_name}_name = '{name}'"
            self.cursor.execute(query)
            id = self.cursor.fetchone()
            if id:
                id = id[0]
            if id is None:
                return None
            return id
        except Exception as e:
            print(e)

    def user_session_id_exists(self, user_session_id) -> bool:
        query = f"SELECT EXISTS (SELECT * FROM user_session WHERE user_session_id = '{user_session_id}')"
        self.cursor.execute(query)
        if self.cursor.fetchone()[0] == 0:
            return False
        return True


    def getTable_user_session(self, user_session_id):
        try:
            query = f"SELECT * FROM user_session WHERE user_session_id = '{user_session_id}'"
            self.cursor.execute(query)
            table = self.cursor.fetchone()
            if table is None:
                return tuple()
            return table
        except Exception as e:
            print(e)


    @staticmethod
    def convert_str_datetime(string_datetime):
        return datetime.datetime.strptime(string_datetime[:-4], '%Y-%m-%d %H:%M:%S')


    def add_category(self, category_name: str, category_parent: str =  'ee7c9258-924f-49d3-b4c8-446541f00dc9'):
        try: 
            # if category_name == None:
            #     raise ValueError("No category name found")
            # elif type(category_name) != str:
            #     raise TypeError("category_name is not a string")
            # elif type(category_parent) != str:
            #     raise TypeError("category_parent is not an string")
            # elif self.fromTable_name_exists('category', category_name):
            #     raise "Category name already exists"
            query = "INSERT INTO CATEGORY (category_parent, category_name) VALUES " \
            f"({category_parent}, '{category_name}');"
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)


    #data can only include category_name, category_parent, category_active
    def modify_category(self, category_id, **data):
        try:
            #Check for errors misinput
            if not self.fromTable_id_exists("category",category_id):
                raise NameError(f"category_id {category_id} does not exist in the database")
            for key in data.keys():
                if key not in ['category_name', 'category_parent', 'category_active']:
                    raise NameError(f"{key} is not an acceptable variable for modify category")
            if 'category_parent' in data.keys() and not type(data['category_parent']) == str:
                raise TypeError("category_parent is should be an integer")
            if 'category_active' in data.keys() and not type(data['category_active']) == int:
                raise TypeError("category_active is should be an integer")
            if 'category_name' in data.keys() and not type(data['category_name']) == str:
                raise TypeError("category_name is should be a string")

            query = self.combine_query('category', category_id, data)
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)


    def add_user(self, user_id, user_name = None):
        try:
            # if self.fromTable_id_exists("user", user_id):
            #     raise NameError("user_id already exists")
            # if user_id == None:
            #     raise ValueError("No value for user_id found")
            
            query = f"INSERT IGNORE INTO user (user_id, user_name) VALUES ({user_id}, '{user_name}')"
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)


    #Only accepts user_name, user_active, user_spent, user_total_active_time
    def modify_user(self, user_id, **data):
        try:
            # if not self.fromTable_id_exists("user", user_id):
            #     raise NameError(f'user_id {user_id} does not exist in the database')
            # for key in data.keys():
            #     if key not in ['user_name', 'user_active', 'user_spent', 'user_total_active_time']:
            #         raise NameError(f"{key} is not an acceptable variable for modify user")
            # if 'user_name' in data.keys() and not type(data['user_name']) == str:
            #     raise TypeError("user_name is not a string")
            # if 'user_active' in data.keys() and not type(data['user_active']) == bool:
            #     raise TypeError("user_active is not a boolean")
            # if 'user_spent' in data.keys() and not type(data['user_spent']) == float:
            #     raise TypeError("user_spent is not a float/double")
            # if 'user_total_active_time' in data.keys() and not type(data['user_total_active_time']) == int:
            #     raise TypeError("user_total_active_time is not an integer")
            
            query = self.combine_query('user', user_id, data)
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)


    def add_brand(self, brand_name):
        try:
            # if self.fromTable_name_exists("brand", brand_name):
            #     raise NameError("brand_name already exists")
            # if brand_name == None:
            #     raise ValueError("No value for brand_name found")

            query = f"INSERT INTO brand (brand_name) VALUES ('{brand_name}');"
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)


    def modify_brand(self, brand_id, **data):
        try:
            # if not self.fromTable_id_exists("brand", brand_id):
            #     raise ValueError("brand_id does not exist")
            # for key in data.keys():
            #     if key not in ['brand_name', 'brand_active']:
            #         raise NameError(f"{key} is not an acceptable variable for modify brand")
            # if 'brand_name' in data.keys() and not type(data['brand_name']) == str:
            #     raise TypeError("brand_name is not a string")
            # if 'brand_active' in data.keys() and not type(data['brand_active']) == bool:
            #     raise TypeError("brand_active should be boolean")
            query = self.combine_query('brand', brand_id, data)
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
    

    def add_event_type(self, event_type_name):
        try:
            # if self.fromTable_name_exists("event_type", event_type_name):
            #     raise NameError("event_type_name already exists")
            # if event_type_name == None:
            #     raise ValueError("No value for event_type_name found")
            
            query = f"INSERT INTO event_type (event_type_name) VALUES ('{event_type_name}');"
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)

    
    def modify_event_type(self, event_type_id, event_type_name):
        try:
            if not self.fromTable_id_exists("event_type", event_type_id):
                raise ValueError("event_type_id does not exist")
            if not type(event_type_name) == str:
                raise TypeError("event_type_name is not a string")

            query = f"UPDATE event_type SET event_type_name = '{event_type_name}' WHERE event_type_id = '{event_type_id}'"
            self.cursor.execute(query)
            self.conn.commit()

        except Exception as e:
            print(e)

    
    def add_user_session(self, user_session_id, user_id, user_session_datetime):
        try:
            user_session_datetime = self.convert_str_datetime(user_session_datetime)

            # if self.user_session_id_exists(user_session_id):
            #     raise ValueError("user_session_id already exists in the database")
            # if not uuid.UUID(str(user_session_id), version=4):
            #     raise TypeError("user_session_id is not an id or a valid id")
            # if not self.fromTable_id_exists("user", user_id):
            #     raise ValueError("user_id does not exist in the database")
            # if not isinstance(user_session_datetime, datetime.datetime):
            #     raise TypeError("user_session_datetime is not a datetime")
        
            query = "INSERT INTO user_session (user_session_id, user_id, user_session_start_time, " \
            f"user_session_end_time) VALUES ('{user_session_id}', {user_id}, '{user_session_datetime}', '{user_session_datetime}')"
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)

    
    def modify_user_session(self, user_session_id, **data):
        try:
            if not self.user_session_id_exists(user_session_id):
                raise ValueError("user_session_id does not exist in the database")
            for key in data.keys():
                if key not in ['user_id', 'user_session_start_time', 'user_session_end_time', 'user_session_active']:
                    raise NameError(f"{key} is not an acceptable variable for modifying user_session")
            if 'user_session_start_time' in data.keys():
                data['user_session_start_time'] = self.convert_str_datetime(data['user_session_start_time'])
                if not isinstance(data['user_session_start_time'], datetime.datetime):
                    raise TypeError("user_session_start_time is not a datetime")
            if 'user_session_end_time' in data.keys():
                data['user_session_end_time'] = self.convert_str_datetime(data['user_session_end_time'])
                if not isinstance(data['user_session_end_time'], datetime.datetime):
                    raise TypeError("user_session_end_time is not a datetime")
            if 'user_id' in data.keys() and not self.fromTable_id_exists('user', data['user_id']):
                raise ValueError("user_id does not exist in the database")
            if 'user_session_active' in data.keys() and not type(data['user_session_active']) == bool:
                raise TypeError("user_session_active is not a boolean")

            query = self.combine_query_strid('user_session', user_session_id, data)
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)


    def add_product(self, product_id: str, product_price: float, brand_id: int = None, category_id = None):
        try:
            # if self.fromTable_id_exists('product', product_id):
            #     raise NameError(f"{product_id} already exists in the database")
            # if brand_id and not self.fromTable_id_exists('brand', brand_id):
            #     raise ValueError(f"{brand_id} brand_id does not exist in the database")
            # if product_price < 0:
            #     raise ValueError("product_price cannot be lower than 0")
            # if product_price is None:
            #     raise ValueError("product needs to have a price")

            if brand_id and category_id:
                query = "INSERT INTO product (product_id, product_price, brand_id, category_id) VALUES " \
                    f"('{product_id}', {product_price}, '{brand_id}', {category_id})"
            elif brand_id:
                query = "INSERT INTO product (product_id, product_price, brand_id) VALUES " \
                    f"('{product_id}', {product_price}, '{brand_id}')"
            elif category_id:
                query = "INSERT INTO product (product_id, product_price, category_id) VALUES " \
                    f"('{product_id}', {product_price}, '{category_id}')"
            else:
                query = "INSERT INTO product (product_id, product_price) VALUES " \
                    f"('{product_id}', {product_price})"
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)


    def modify_product(self, product_id, **data):
        try:
            if not self.fromTable_id_exists('product', product_id):
                raise ValueError("product_id does not exist in the database")
            for key in data.keys():
                if key not in ['product_name', 'product_price', 'brand_id', 'product_active']:
                    raise NameError(f"{key} is not an acceptable variable for modifying product")
            if 'product_name' in data.keys() and (type(data['product_name']) != str or data["product_name"] == None):
                raise TypeError("product_name is not a string")
            if 'product_price' in data.keys() and type(data['product_price']) != float:
                raise TypeError("product_price is not a float")
            if 'brand_id' in data.keys():
                if not self.fromTable_id_exists('brand', data['brand_id']):
                    raise ValueError(f"The brand_id {data['brand_id']} does not exist in the database")
                if type(data['brand_id']) != str:
                    raise TypeError("brand_id is not an string")
            if 'product_active' in data.keys() and type(data['product_active']) != bool:
                raise TypeError("product_active is not a boolean")
            query = self.combine_query('product', product_id, data)
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)


    def add_user_activity(self, user_id: int, event_type: str, product_id: int, user_session_id: str,
    event_time: datetime.datetime, category_id:int = None):
        try:
            # if not self.fromTable_id_exists('user', user_id):
            #     raise ValueError("User does not exist in the database")
            # if not self.fromTable_name_exists("event_type", event_type):
            #     raise ValueError("event_type does not exist")
            # if not self.fromTable_id_exists("product", product_id):
            #     raise ValueError("product_id does not exist in the database")
            # if not self.user_session_id_exists(user_session_id):
            #     raise ValueError("user_session_id does not exist")
            # if category_id and not self.fromTable_id_exists('category',category_id):
            #     raise ValueError("category_id does not exist in the database")
            if event_type == "view":
                event_type_id = 1
            elif event_type == "cart":
                event_type_id = 2
            elif event_type == "remove_from_cart":
                event_type_id = 3
            else:
                event_type_id = 4
            if category_id: 
                query = "INSERT INTO user_activity (event_time, event_type_id, product_id, category_id, " \
                    "user_id, user_session_id) VALUES " \
                        f"('{self.convert_str_datetime(event_time)}', {event_type_id}, {product_id}, {category_id}, {user_id}, '{user_session_id}')"
            else:
                query = "INSERT INTO user_activity (event_time, event_type_id, product_id, " \
                    "user_id, user_session_id) VALUES " \
                        f"('{self.convert_str_datetime(event_time)}', {event_type_id}, {product_id}, {user_id}, '{user_session_id}')"

            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)

    
    def modify_user_activity(self, user_id, **data):
        try:
            pass
        except Exception as e:
            print(e)


    def getUserSession_between_date_exists(self, user_id, start_date, end_date) -> bool:
        try:
            pass
        except Exception as e:
            print(e)

    
    def user_add_purchase(self, user_id, user_spent):
        try:
            # if not self.fromTable_id_exists('user', user_id):
            #     raise ValueError("User_id does not exist in the database")
            # if user_spent < 0:
            #     raise ValueError("user_spent cannot be less than 0")
            query = f"UPDATE user SET user_spent = user_spent + {user_spent} WHERE user_id = {user_id}"
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)


    def user_add_active_time(self, user_id, amount_time):
        try:
            # if not self.fromTable_id_exists('user', user_id):
            #     raise ValueError("User_id does not exist in the database")
            # if amount_time < 0:
            #     raise ValueError("amount_time cannot be less than 0")
            query = f"UPDATE user SET user_total_active_time = user_total_active_time + {amount_time} WHERE user_id = {user_id}"
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)

    
    def product_add_event_type(self, product_id, event_type_name, user_id):
        try:
            # if not self.fromTable_id_exists('product', product_id):
            #     raise ValueError("product_id does not exist in the database")
            # if not self.fromTable_name_exists('event_type', event_type_name):
            #     raise ValueError("event_type_name does not exist in the database")

            if event_type_name == "view":
                event_type_name = "view"
            elif event_type_name == "cart":
                event_type_name = "add_cart"
            elif event_type_name == "remove_from_cart":
                event_type_name = "removed_cart"
            else:
                event_type_name = "purchase"
                price = self.getTable_from_id('product', product_id)[2]
                data = {"user_spent": price}
                self.modify_user(user_id, **data)


            query = f"INSERT INTO product_{event_type_name} (product_id, user_id) VALUES ({product_id}, {user_id})"
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)

    @staticmethod
    def parse_category(category: str):
        try:
            categories = category.split('.')
            return categories
        except Exception as e:
            print(e)


    def batch_product_event(self, batch_product_event):
        try:
            # if not self.fromTable_id_exists('product', product_id):
            #     raise ValueError("product_id does not exist in the database")
            # if not self.fromTable_name_exists('event_type', event_type_name):
            #     raise ValueError("event_type_name does not exist in the database")
            query_view = "INSERT INTO product_view (product_id, user_id) VALUES "
            query_add_cart = "INSERT INTO product_add_cart (product_id, user_id) VALUES "
            query_purchase = "INSERT INTO product_purchase (product_id, user_id) VALUES "
            query_remove_cart = "INSERT INTO product_remove_cart (product_id, user_id) VALUES "
            for product_event in batch_product_event:
                if product_event['event_type'] == "view":
                    product_event['event_type'] = "view"
                    query_view += f"({product_event['product_id']}, {product_event['user_id']}), "
                elif product_event['event_type'] == "cart":
                    product_event['event_type'] = "add_cart"
                    query_add_cart += f"({product_event['product_id']}, {product_event['user_id']}), "
                elif product_event['event_type'] == "remove_from_cart":
                    product_event['event_type'] = "removed_cart"
                    query_remove_cart += f"({product_event['product_id']}, {product_event['user_id']}), "
                else:
                    product_event['event_type'] = "purchase"
                    price = product_event['price']
                    query_purchase += f"({product_event['product_id']}, {product_event['user_id']}), "
                    data = {"user_spent": price}
                    self.modify_user(product_event['user_id'], **data)

            if query_view[-2:] == ", ":
                query_view = query_view[:-2]
                self.cursor.execute(query_view)
            if query_add_cart[-2:] == ", ":
                query_add_cart = query_add_cart[:-2]
                self.cursor.execute(query_add_cart)
            if query_purchase[-2:] == ", ":
                query_purchase = query_purchase[:-2]
                self.cursor.execute(query_purchase)
            if query_remove_cart[-2:] == ", ":
                query_remove_cart = query_remove_cart[:-2]
                self.cursor.execute(query_remove_cart)
            self.conn.commit()
        except Exception as e:
            print(e)


    def batch_user_activity(self, batch_user_activity):
        query = "INSERT INTO user_activity (user_id, event_type_id, product_id, user_session_id, event_time) VALUES "

        for user_activity in batch_user_activity:
            if user_activity['event_type'] == "view":
                event_type_id = 1
            elif user_activity['event_type'] == "cart":
                event_type_id = 2
            elif user_activity['event_type'] == "remove_from_cart":
                event_type_id = 3
            else:
                event_type_id = 4

            if type(user_activity['event_time']) == str:
                self.convert_str_datetime(user_activity['event_time'])
            query += f"({user_activity['user_id']}, {event_type_id}, {user_activity['product_id']}," \
            f"'{user_activity['user_session_id']}', '{user_activity['event_time']}'), " 

        if query[-2:] == ", ":
            query = query[:-2]
            self.cursor.execute(query)
            self.conn.commit()
