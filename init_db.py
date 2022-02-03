import sys
import mysql.connector

HOST_IP = "127.0.0.1"

prod_db = mysql.connector.connect(
    host="localhost",
    user="prod",
    password="prodpassword"
)

if __name__ == "__main__":

    if(len(sys.argv) < 2):
        print("Usage: " + sys.argv[0] + " <database name>")
        exit()

    db_name = sys.argv[1]
    db_cursor = prod_db.cursor()
    db_cursor.execute("CREATE DATABASE " + db_name)