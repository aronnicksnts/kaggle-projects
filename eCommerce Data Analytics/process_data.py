### PROCESSES DATA FROM \data AND PUTS IT INTO THE DATABASE

from unicodedata import category
import sql_commands as sql
import datetime
import uuid
import os
import glob
import pandas as pd

mySQL = sql.SQL()
# files = glob.glob(os.path.join(os.getcwd()+"\\data", "*.csv"))

# for file in files:
#     for df in pd.read_csv(file, header=None, chunksize=10000):
#         print(df.iloc[1])

mySQL.user_add_purchase(503, -100)
mySQL.user_add_purchase(503, 100)
