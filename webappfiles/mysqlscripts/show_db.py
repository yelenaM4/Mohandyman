import mysql.connector
import dbconnect

cur, con = dbconnect.get_connection()

cur.execute("SHOW DATABASES")

for x in cur:
    print(x)