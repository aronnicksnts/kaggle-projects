from datetime import datetime
from sqlite3 import connect
import mysql.connector
from mysql.connector import Error
import json
import uuid
import datetime
import logging

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
        return uuid.uuid1().int>>64


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
            return self.cursor.fetchall()[0][0]
            

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


    def add_category(self, category_name: str, category_parent: int =  0):
        try: 
            if category_name == None:
                raise ValueError("No category name found")
            elif type(category_name) != str:
                raise TypeError("category_name is not a string")
            elif type(category_parent) != int:
                raise TypeError("category_parent is not an integer")
            elif self.fromTable_name_exists('category', category_name):
                raise "Category name already exists"
            category_id = self.generate_random_number()
            query = "INSERT INTO CATEGORY (category_id, category_parent, category_name) VALUES " \
            f"({category_id}, {category_parent}, '{category_name}');"
            self.cursor.execute(query)
            self.conn.commit()
            print(f"Successfully added {category_name} into category")
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
            if 'category_parent' in data.keys() and not type(data['category_parent']) == int:
                raise TypeError("category_parent is should be an integer")
            if 'category_active' in data.keys() and not type(data['category_active']) == int:
                raise TypeError("category_active is should be an integer")
            if 'category_name' in data.keys() and not type(data['category_name']) == str:
                raise TypeError("category_name is should be a string")

            query = self.combine_query('category', category_id, data)
            self.cursor.execute(query)
            self.conn.commit()

            print("Sucessfully modified category")
        except Exception as e:
            print(e)


    def add_user(self, user_id, user_name = None):
        try:
            if self.fromTable_id_exists("user", user_id):
                raise NameError("user_id already exists")
            if user_id == None:
                raise ValueError("No value for user_id found")
            
            query = f"INSERT INTO user (user_id, user_name) VALUES ({user_id}, '{user_name}')"
            self.cursor.execute(query)
            self.conn.commit()
            print(f"Successfully added User {user_id}")
        except Exception as e:
            print(e)


    #Only accepts user_name, user_active, user_spent, user_total_active_time
    def modify_user(self, user_id, **data):
        try:
            if not self.fromTable_id_exists("user", user_id):
                raise NameError(f'user_id {user_id} does not exist in the database')
            for key in data.keys():
                if key not in ['user_name', 'user_active', 'user_spent', 'user_total_active_time']:
                    raise NameError(f"{key} is not an acceptable variable for modify user")
            if 'user_name' in data.keys() and not type(data['user_name']) == str:
                raise TypeError("user_name is not a string")
            if 'user_active' in data.keys() and not type(data['user_active']) == bool:
                raise TypeError("user_active is not a boolean")
            if 'user_spent' in data.keys() and not type(data['user_spent']) == float:
                raise TypeError("user_spent is not a float/double")
            if 'user_total_active_time' in data.keys() and not type(data['user_total_active_time']) == int:
                raise TypeError("user_total_active_time is not an integer")
            
            query = self.combine_query('user', user_id, data)
            self.cursor.execute(query)
            self.conn.commit()

            print("Successfully Modified User")
        except Exception as e:
            print(e)


    def add_brand(self, brand_name):
        try:
            if self.fromTable_name_exists("brand", brand_name):
                raise NameError("brand_name already exists")
            if brand_name == None:
                raise ValueError("No value for brand_name found")
            
            brand_id = self.generate_random_number()
            query = f"INSERT INTO brand (brand_id, brand_name) VALUES ({brand_id}, '{brand_name}');"
            print(query)
            self.cursor.execute(query)
            self.conn.commit()
            print(f"Successfully added brand {brand_name}")
        except Exception as e:
            print(e)


    def modify_brand(self, brand_id, **data):
        try:
            if not self.fromTable_id_exists("brand", brand_id):
                raise ValueError("brand_id does not exist")
            for key in data.keys():
                if key not in ['brand_name', 'brand_active']:
                    raise NameError(f"{key} is not an acceptable variable for modify brand")
            if 'brand_name' in data.keys() and not type(data['brand_name']) == str:
                raise TypeError("brand_name is not a string")
            if 'brand_active' in data.keys() and not type(data['brand_active']) == bool:
                raise TypeError("brand_active should be boolean")
            query = self.combine_query('brand', brand_id, data)
            self.cursor.execute(query)
            self.conn.commit()
            print("Modified brand successfully")
        except Exception as e:
            print(e)
    

    def add_event_type(self, event_type_name):
        try:
            if self.fromTable_name_exists("event_type", event_type_name):
                raise NameError("event_type_name already exists")
            if event_type_name == None:
                raise ValueError("No value for event_type_name found")
            
            event_type_id = self.generate_random_number()
            query = f"INSERT INTO event_type (event_type_id, event_type_name) VALUES ({event_type_id}, '{event_type_name}');"
            print(query)
            self.cursor.execute(query)
            self.conn.commit()
            print(f"Successfully added event_type {event_type_name}")
        except Exception as e:
            print(e)

    
    def modify_event_type(self, event_type_id, event_type_name):
        try:
            if not self.fromTable_id_exists("event_type", event_type_id):
                raise ValueError("event_type_id does not exist")
            if not type(event_type_name) == str:
                raise TypeError("event_type_name is not a string")

            query = f"UPDATE event_type SET event_type_name = '{event_type_name}' WHERE event_type_id = {event_type_id}"
            self.cursor.execute(query)
            self.conn.commit()
            print("Modified event_type successfully")

        except Exception as e:
            print(e)

    
    def add_user_session(self, user_session_id, user_id, user_session_datetime):
        try:
            if self.fromTable_id_exists("user_session", user_session_id):
                raise ValueError("user_session_id already exists in the database")
            if not type(user_session_id) == str and len(user_session_id) == 36:
                raise TypeError("user_session_id is not an id")
            if not self.fromTable_id_exists("user", user_id):
                raise ValueError("user_id does not exist in the database")
            if not isinstance(user_session_datetime, datetime.datetime):
                raise TypeError("user_session_datetime is not a datetime")
            
            query = "INSERT INTO user_session (user_session_id, user_id, user_session_start_time, " \
            f"user_session_end_time) VALUES ({user_session_id}, {user_id}, {user_session_datetime}, {user_session_datetime})"
            self.cursor.execute(query)
            self.conn.commit()
            print("Added user_session successfully")
        except Exception as e:
            print(e)

    
    def modify_user_session(self, user_session_id, **data):
        try:
            pass
        except Exception as e:
            print(e)


    def add_product(self, product_name, **data):
        try:
            pass
        except Exception as e:
            print(e)


    def modify_product(self, product_id, **data):
        try:
            pass
        except Exception as e:
            print(e)


    def getUserSession_between_date_exists(self, user_id, start_date, end_date) -> bool:
        try:
            pass
        except Exception as e:
            print(e)

    
    def add_user_activity(self, user_id, **data):
        try:
            pass
        except Exception as e:
            print(e)

    
    def modify_user_activity(self, user_id, **data):
        try:
            pass
        except Exception as e:
            print(e)
