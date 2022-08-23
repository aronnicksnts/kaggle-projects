from unicodedata import category
import sql_commands as sql
import datetime
import uuid

mySQL = sql.SQL()

data = {'user_session_end_time': '2022-11-02 05:05:05 UTC','user_id': 100}
mySQL.add_user(100)
mySQL.modify_user_session('1336d9ce-da30-4d8b-9073-23872752cd27', **data)
