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

# TODO: increment number of items sold by seller

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

            item_name = tokens[1]
            item_category = tokens[2]
            item_keywords = tokens[3]
            item_condition = tokens[4]
            item_price = tokens[5]
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
                            + "(\"" + item_name + "\", " + item_category + ", " \
                            + str(new_id) + ", " + "\"" + item_keywords + "\", " \
                            + item_condition + ", " + item_price + ", " + u_id + ");"

                print(sql_query)
                db_cursor.execute(sql_query)
                data = "Item listed successfully."
                prod_db.commit()

        elif(command == "modify"):

            item_id = tokens[1]
            new_price = tokens[2]
            u_id = tokens[3]

            if(int(u_id) == -1):
                data = "User is not logged in."
                
            else:
                sql_query = "UPDATE products SET price=" + new_price + " WHERE id=" + item_id + " AND s_id=" + u_id + ";"
                db_cursor.execute(sql_query)
                data = "Price updated successfully."
                prod_db.commit()

        elif(command == "remove"):

            item_id = tokens[1]
            item_quantity = tokens[2]
            u_id = tokens[3]

            if(int(u_id) == -1):
                data = "User is not logged in."

            else:
                sql_query = "DELETE FROM products WHERE id=" + item_id + " AND s_id=" + u_id + " LIMIT " + item_quantity + ";"
                db_cursor.execute(sql_query)
                data = "Entry removed."
                prod_db.commit()

        elif(command == "list"):

            u_id = tokens[1]
            if(int(u_id) == -1):
                data = "User is not logged in."

            else:
                db_cursor.execute("SELECT * FROM products WHERE s_id=" + u_id + ";")
                data = ""
                for x in db_cursor:
                    data += str(x) + "\n"
                if(len(data) == 0):
                    data = "Database is empty."

        elif(command == "create"):

            # TODO: handle collisions?
            #       Username + password combo already exists?

            # get current highest user ID


            name = tokens[1]
            password = tokens[2]

            cus_cursor.execute("SELECT MAX(id) FROM customer.users;")
            data = ""

            new_id = 0
            for x in cus_cursor:
                if(isinstance(x[0], int)):
                    new_id = x[0]+1


            sql_query = "INSERT INTO users " \
                        + "(name, id, nitems) " \
                        + "VALUES " \
                        + "(\"" + name + "\", " + str(new_id) + ", " + "0);"

            cus_cursor.execute(sql_query)

            sql_query = "INSERT INTO passwords "\
                        + "(id, password) " \
                        + "VALUES " \
                        + "(" + str(new_id) + ", " + "\"" + password + "\")"

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

            