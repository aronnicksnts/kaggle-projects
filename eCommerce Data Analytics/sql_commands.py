from datetime import datetime
from itertools import product
from multiprocessing.sharedctypes import Value
from sqlite3 import connect
from tokenize import Double
from unicodedata import category
import mysql.connector
from mysql.connector import Error
import json
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

    def createNewDate(self, date: datetime.datetime):
        dateNum = date.date()
        monthNum = dateNum.month
        monthName = dateNum.strftime("%B")
        monthShortName = dateNum.strftime("%b")
        dayNum = dateNum.day
        dayOfWeek = dateNum.weekday()
        yearNum = dateNum.year
        quarter = ((dateNum.month-1) // 3) + 1

        query = "INSERT INTO DIM_DATE (dateNum, monthNum, monthName, monthShortName, dayNum, dayOfWeek," \
            f"yearNum, quarter) VALUES ('{dateNum}', {monthNum}, '{monthName}', '{monthShortName}', {dayNum}, " \
                f"{dayOfWeek}, {yearNum}, {quarter})"
        print(query)
        self.cursor.execute(query)
        self.conn.commit()

    def checkDateExists(self, date: datetime.datetime) -> bool:
        date = date.date()
        query = f"SELECT EXISTS (SELECT * FROM Dim_Date WHERE dateNum = '{date}')"
        self.cursor.execute(query)
        if self.cursor.fetchone()[0] == 0:
                return False
        return True

    def getDateKey(self, date):
        date = date.date()
        query = f"SELECT dateKey FROM Dim_Date WHERE dateNum = '{date}'"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]


    def getDateTable(self, dateKey):
        query = f"SELECT * FROM Dim_Date WHERE dateKey = '{dateKey}'"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def createNewProduct(self, productId, categoryId, price, categoryName = None, brand = None):
        queryList = ["productId", "categoryId", "price"]
        queryValue = [productId, categoryId, price]
        if categoryName:
            queryList.append("categoryName")
            queryValue.append(categoryName)
        if brand:
            queryList.append("brand")
            queryValue.append(brand)

        query = "INSERT INTO dim_product ("
        for column in queryList:
            query += f"{column}, "
        query = query[:-2] + ") VALUES ("

        for column in queryValue:
            if type(column) != str:
                query += f"{column}, "
            else:
                query += f"'{column}', "
        query = query[:-2] + ")"
        self.cursor.execute(query)
        self.conn.commit()

    def checkProductExists(self, productId) -> bool:
        query = f"SELECT EXISTS (SELECT * FROM dim_product WHERE productId = '{productId}' AND activeFlag = 1)"
        self.cursor.execute(query)
        if self.cursor.fetchone()[0] == 0:
                return False
        return True

    def getProductTable(self, productId):
        query = f"SELECT * FROM dim_product WHERE productId = '{productId}' AND activeFlag = 1"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def checkProductChange(self, productId, categoryName= None, categoryId= None, brand= None, price= None):
        pass

    def disableProduct(self, productId):
        pass

