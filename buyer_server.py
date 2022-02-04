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

        data = ""
        if command == "search":
            sql_query = "SELECT * FROM products " \
                        "WHERE category = " + tokens[1]+" AND keywords LIKE '%" + tokens[2] + "%';"
            print(sql_query)
            db_cursor.execute(sql_query)
            result = db_cursor.fetchall()
            data = ""
            for x in result:
                data += str(x) + "\n"
            if len(data) == 0:
                data = "No matching data found."
            print(data)
        elif command == "add":
            pre_query = "SELECT id FROM cart WHERE id = "+tokens[1] + ";"
            db_cursor.execute(pre_query)
            if db_cursor.rowcount == 0:
                sql_query = "INSERT INTO cart VALUES(" + tokens[1] + "," + tokens[2] + ");"
                new_cursor = prod_db.cursor()
                new_cursor.execute(sql_query)
                if new_cursor.rowcount > 0:
                    data = "Item added successfully."
                else:
                    data = "Item could not be added"
            else:
                sql_query = "UPDATE cart SET quantity = quantity+" + tokens[2] \
                        + " WHERE id = " + tokens[1] + ";"
                print(sql_query)
                new_cursor = prod_db.cursor()
                new_cursor.execute(sql_query)
                if new_cursor.rowcount > 0:
                    data = "Item added successfully."
                else:
                    data = "Item could not be added"
            prod_db.commit()
        elif command == "remove":
            sql_query = "UPDATE cart SET quantity = quantity-" + tokens[2] \
                        + " WHERE id = " + tokens[1] + " AND quantity-" + tokens[2] + ">=0;"
            print(sql_query)
            db_cursor.execute(sql_query)
            prod_db.commit()
            if db_cursor.rowcount > 0:
                data = "Item(s) removed successfully."
            else:
                data = "Item(s) could not be removed"
        elif command == "clear":
            sql_query = "DELETE FROM cart;"
            print(sql_query)
            db_cursor.execute(sql_query)
            prod_db.commit()
            if db_cursor.rowcount > 0:
                data = "Cart cleared successfully."
            else:
                data = "Cart could not be cleared"
        elif command == "display":
            sql_query = "SELECT * FROM cart;"
            db_cursor.execute(sql_query)
            result = db_cursor.fetchall()
            data = ""
            for x in result:
                data += str(x) + "\n"
            if len(data) == 0:
                data = "Your cart is empty."
            print(data)
        else:
            data = "ERROR"

        # try/except wrapper to prevent error logging on the server
        try:
            conn.sendall(data.encode('utf-8'))
        except:
            pass

    # close connection after broken pipe
    conn.close()


if __name__ == "__main__":

    db_cursor = prod_db.cursor(buffered=True)

    if (len(sys.argv) < 2):
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
