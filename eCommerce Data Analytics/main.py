from unicodedata import category
import sql_commands as sql

mySQL = sql.SQL()

# mySQL.add_category("kitchen")
print(mySQL.getTable_from_id("category", 1))
