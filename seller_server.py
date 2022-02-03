import sys
import socket
import mysql.connector
from _thread import *
import threading

HOST_IP = "127.0.0.1"

prod_db = mysql.connector.connect(
    host="localhost",
    user="prod",
    password="prodpassword",
    database="product"
)

# Handler for new connection
# Connects to database to run commands
# Closes connection upon termination
def thread_handler(conn):
    while True:
        data = conn.recv(1024)
        data = data.decode('utf-8')
        tokens = data.split('\n')
        command = tokens[0]

        if(command == "sell"):

            sql_query = "INSERT INTO products " \
                        + "(name, category, id, keywords, item_condition, price) " \
                        + "VALUES " \
                        + "(\"" + tokens[1] + "\", " + tokens[2] + ", " \
                        + tokens[3] + ", " + "\"" + tokens[4] + "\", " \
                        + tokens[5] + ", " + tokens[6] + ");"

            print(sql_query)
            db_cursor.execute(sql_query)
            data = "Item listed successfully."

        elif(command == "modify"):
            sql_query = "UPDATE products SET price=" + tokens[2] + " WHERE id=" + tokens[1] + ";"
            db_cursor.execute(sql_query)
            data = "Price updated successfully."

        elif(command == "remove"):
            sql_query = "DELETE FROM products WHERE id=" + tokens[1] + " LIMIT " + tokens[2] + ";"
            db_cursor.execute(sql_query)
            data = "Entry removed."

        elif(command == "list"):
            db_cursor.execute("SELECT * FROM products;")
            data = ""
            for x in db_cursor:
                data += str(x) + "\n"
            if(len(data) == 0):
                data = "Database is empty."
        else:
            data = "ERROR"

        # try/except wrapper to prevent error loggin on the server
        try:
            conn.sendall(data.encode('utf-8'))
        except:
            pass
    
    # close connection after broken pipe
    conn.close()

if __name__ == "__main__":

    db_cursor = prod_db.cursor()

    if(len(sys.argv) < 2):
        print("Usage: %s <port>" % sys.argv[0])
        exit()

    PORT = int(sys.argv[1])

    # initialize socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST_IP, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        start_new_thread(thread_handler, (conn,))
    s.close()

            