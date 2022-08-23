from unicodedata import category
import sql_commands as sql
import datetime
import uuid

mySQL = sql.SQL()

mySQL.add_user_session(uuid.uuid4(), 503, '2019-11-01 00:00:00 UTC')
