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

cus_db = mysql.connector.connect(
    host="localhost",
    user="prod",
    password="prodpassword",
    database="customer"
)

# TODO: 
#   register seller ID in the product database 
#       (buyers provide feedback on ITEMS, need to tie items to sellers)
#   make item IDs generated server-side, not client defined

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

            u_id = tokens[6]
            if(int(u_id) == -1):
                data = "User is not logged in."

            else:
                db_cursor.execute("SELECT MAX(id) FROM products;")
                data = ""

                new_id = 0
                for x in db_cursor:
                    if(isinstance(x[0], int)):
                        new_id = x[0]+1

                sql_query = "INSERT INTO products " \
                            + "(name, category, id, keywords, item_condition, price, s_id) " \
                            + "VALUES " \
                            + "(\"" + tokens[1] + "\", " + tokens[2] + ", " \
                            + str(new_id) + ", " + "\"" + tokens[3] + "\", " \
                            + tokens[4] + ", " + tokens[5] + ", " + tokens[6] + ");"

                print(sql_query)
                db_cursor.execute(sql_query)
                data = "Item listed successfully."
                prod_db.commit()

        elif(command == "modify"):
            sql_query = "UPDATE products SET price=" + tokens[2] + " WHERE id=" + tokens[1] + ";"
            db_cursor.execute(sql_query)
            data = "Price updated successfully."
            prod_db.commit()

        elif(command == "remove"):
            sql_query = "DELETE FROM products WHERE id=" + tokens[1] + " LIMIT " + tokens[2] + ";"
            db_cursor.execute(sql_query)
            data = "Entry removed."
            prod_db.commit()

        elif(command == "list"):
            u_id = tokens[1]
            if(int(u_id) == -1):
                data = "User is not logged in."
            else:
                db_cursor.execute("SELECT * FROM products WHERE s_id=" + tokens[1] + ";")
                data = ""
                for x in db_cursor:
                    data += str(x) + "\n"
                if(len(data) == 0):
                    data = "Database is empty."

        elif(command == "create"):

            # TODO: handle collisions?
            #       Username + password combo already exists?

            # get current highest user ID
            cus_cursor.execute("SELECT MAX(id) FROM customer.users;")
            data = ""

            new_id = 0
            for x in cus_cursor:
                if(isinstance(x[0], int)):
                    new_id = x[0]+1


            sql_query = "INSERT INTO users " \
                        + "(name, id, nitems) " \
                        + "VALUES " \
                        + "(\"" + tokens[1] + "\", " + str(new_id) + ", " + "0);"

            cus_cursor.execute(sql_query)

            sql_query = "INSERT INTO passwords "\
                        + "(id, password) " \
                        + "VALUES " \
                        + "(" + str(new_id) + ", " + "\"" + tokens[2] + "\")"

            cus_cursor.execute(sql_query)

            sql_query = "INSERT INTO feedback "\
                        + "(id, pos, neg) " \
                        + "VALUES " \
                        + "(" + str(new_id) + ", 0, 0);"

            cus_cursor.execute(sql_query)


            # logged table might be useless if we are using client side cookies to track login
            sql_query = "INSERT INTO logged "\
                        + "(id, logged) " \
                        + "VALUES " \
                        + "(" + str(new_id) + ", 0);"

            cus_cursor.execute(sql_query)

            data = "Customer added successfully."
            cus_db.commit()

        elif(command == "login"):

            username = tokens[1]
            password = tokens[2]

            # join passwords to users on ID
            # select user id that matches both username and password
            sql_query = "SELECT users.id FROM users " \
                        + "INNER JOIN passwords ON users.id=passwords.id " \
                        + "WHERE passwords.password = \"" + password + "\" " \
                        + "and users.name = \"" + username +"\";"

            cus_cursor.execute(sql_query)

            # get the returned user id
            # u_id will be -1 if no matching user is found
            u_id = -1
            for x in cus_cursor:
                if(isinstance(x[0], int)):
                    u_id = x[0]


            # if user exists, set their status to logged in
            if(u_id != -1):
                sql_query = "UPDATE logged SET logged=1 WHERE id=" + str(u_id) + ";"
                cus_cursor.execute(sql_query)

            cus_db.commit()
            data = str(u_id)


        elif(command == "logout"):

            u_id = tokens[1]
            if(int(u_id) == -1):
                data = "User is not logged in."
            else:
                sql_query = "UPDATE logged SET logged=0 WHERE id=" + u_id + ";"
                cus_cursor.execute(sql_query)
                cus_db.commit()
                data = "Logged out."

        elif(command == "rating"):

            u_id = tokens[1]
            if(int(u_id) == -1):
                data = "User is not logged in."
            else:
                sql_query = "SELECT * FROM feedback WHERE id=" + u_id + ";"
                cus_cursor.execute(sql_query)

                data = ""
                for x in cus_cursor:
                    data += str(x) + "\n"

                if(data == ""):
                    data = "User has no ratings."

        else:
            data = "ERROR"

        # try/except wrapper to prevent error logging on the server
        try:
            conn.sendall(data.encode('utf-8'))
        except:
            break
    
    # close connection after broken pipe
    conn.close()

if __name__ == "__main__":

    db_cursor = prod_db.cursor(buffered=True)
    cus_cursor = cus_db.cursor(buffered=True)

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

            