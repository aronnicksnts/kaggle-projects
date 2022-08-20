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

    def generate_random_number(self):
        return uuid.uuid1().int>>64

    def generate_random_id(self):
        return str(uuid.uuid4())

    def add_category(self, category_name: str, category_parent: int =  0):
        try: 
            if category_name == None:
                raise ValueError("No category name found")
            elif type(category_name) != str:
                raise TypeError("category_name is not a string")
            elif type(category_parent) != int:
                raise TypeError("category_parent is not an integer")
            category_id = self.generate_random_number()
            if category_parent == 0:
                query = "INSERT INTO CATEGORY (category_id, category_name) VALUES " \
                    f"({category_id}, '{category_name}')"
            else:
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
            if not self.table_id_exists("category",category_id):
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

            query = "UPDATE CATEGORY SET "
            for (key, value) in data.items():
                if type(value) == int:
                    query += f"{key} = {value}, "
                else:
                    query += f"{key} = '{value}', "
            query = query[:-2] + f" WHERE category_id = {category_id}"
            print(query)
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
    

    def table_id_exists(self, table_name, id) -> bool:
        query = f"SELECT EXISTS (SELECT * FROM {table_name} WHERE {table_name}_id = {id})"
        print(query)
        self.cursor.execute(query)
        return self.cursor.fetchall()[0][0]


