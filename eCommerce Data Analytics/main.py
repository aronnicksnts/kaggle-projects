from unicodedata import category
import sql_commands as sql

mySQL = sql.SQL()

mySQL.modify_event_type(8549804432497906157, "Purchase")
