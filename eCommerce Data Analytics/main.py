from unicodedata import category
import sql_commands as sql
import datetime
import uuid

mySQL = sql.SQL()
data = {'product_price': 1.06}
mySQL.modify_product(1003461, **data)