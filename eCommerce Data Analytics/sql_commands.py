from sqlite3 import connect
import mysql.connector
from mysql.connector import Error
import json
import uuid

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
    def add_category(self, category_name: str, category_parent: int =  0):
        try: 
            if category_name == None:
                raise ValueError("No category name found")
            elif type(category_name) != str:
                raise TypeError("category_name is not a string")
            elif type(category_parent) != int:
                raise TypeError("category_parent is not an integer")
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
        except Exception as e:
            print(e)

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
        return self.cursor.fetchall()[0][0]

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

    def add_user(self, user_id, user_name):
        try:
            if not self.fromTable_id_exists("user", user_id):
                raise "user_id already exists"
            
            query = f"INSERT INTO user (user_id, user_name) VALUES ({user_id}, '{user_name}')"
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)

    #Only accepts user_name, user_active, user_spent, user_total_active_time
    def modify_user(self, user_id, **data):
        try:
            if not self.fromTable_id_exists("user", user_id):
                raise NameError(f'user_id {user_id} does not exist in the database')
            for key in data.keys():
                if key not in ['user_name', 'user_active', 'user_spent', 'user_total_active_time']:
                    raise NameError(f"{key} is not an acceptable variable for modify category")
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

        except Exception as e:
            print(e)

