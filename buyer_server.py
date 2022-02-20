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

            u_id = tokens[3]
            if(int(u_id) == -1):
                data = "User is not logged in."

            else:
                pre_query = "SELECT id FROM cart WHERE id = "+tokens[1] + " AND b_id=" + u_id + ";"
                db_cursor.execute(pre_query)
                if db_cursor.rowcount == 0:
                    sql_query = "INSERT INTO cart VALUES(" + tokens[1] + "," + u_id + "," + tokens[2] + ");"
                    new_cursor = prod_db.cursor()
                    new_cursor.execute(sql_query)
                    if new_cursor.rowcount > 0:
                        data = "Item added successfully."
                    else:
                        data = "Item could not be added"
                else:
                    sql_query = "UPDATE cart SET quantity = quantity+" + tokens[2] \
                            + " WHERE id = " + tokens[1] + " AND b_id=" + u_id + ";"
                    print(sql_query)
                    new_cursor = prod_db.cursor()
                    new_cursor.execute(sql_query)
                    if new_cursor.rowcount > 0:
                        data = "Item added successfully."
                    else:
                        data = "Item could not be added"
                prod_db.commit()

        elif command == "remove":

            u_id = tokens[3]
            if(int(u_id) == -1):
                data = "User is not logged in."

            else:
                sql_query = "UPDATE cart SET quantity = quantity-" + tokens[2] \
                            + " WHERE id = " + tokens[1] + " AND quantity-" \
                            + tokens[2] + ">=0" + " AND b_id=" + u_id + ";"
                print(sql_query)
                db_cursor.execute(sql_query)
                prod_db.commit()
                if db_cursor.rowcount > 0:
                    data = "Item(s) removed successfully."
                else:
                    data = "Item(s) could not be removed"

        elif command == "clear":

            u_id = tokens[1]
            if(int(u_id) == -1):
                data = "User is not logged in."

            else:
                sql_query = "DELETE FROM cart WHERE b_id=" + u_id + ";"
                print(sql_query)
                db_cursor.execute(sql_query)
                prod_db.commit()
                if db_cursor.rowcount > 0:
                    data = "Cart cleared successfully."
                else:
                    data = "Cart could not be cleared"

        elif command == "display":

            u_id = tokens[1]
            if(int(u_id) == -1):
                data = "User is not logged in."

            else:
                sql_query = "SELECT * FROM cart WHERE b_id=" + u_id + ";"
                db_cursor.execute(sql_query)
                result = db_cursor.fetchall()
                data = ""
                for x in result:
                    data += str(x) + "\n"
                if len(data) == 0:
                    data = "Your cart is empty."
                print(data)

        elif command == "create":
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

        elif command == "login":

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

        elif command == "logout":

            u_id = tokens[1]
            if(int(u_id) == -1):
                data = "User is not logged in."
            else:
                sql_query = "UPDATE logged SET logged=0 WHERE id=" + u_id + ";"
                cus_cursor.execute(sql_query)
                cus_db.commit()
                data = "Logged out."

        elif command == "purchase":

            u_id = tokens[4]
            if(int(u_id) == -1):
                data = "User is not logged in."

            # send purchase request to third party

            # if invalid, exit

            # if valid, add item to purchase table FROM CART

            sql_query = "INSERT INTO customer.purchased (id, b_id, quantity) " \
                        + "SELECT id, b_id, quantity FROM product.cart WHERE product.cart.b_id=" \
                        + u_id + ";"

            cus_cursor.execute(sql_query)
            cus_db.commit()

            # clear cart
            sql_query = "DELETE FROM product.cart WHERE b_id=" + u_id + ";"

            db_cursor.execute(sql_query)

            prod_db.commit()
            data = "Items have been purchased!"

            # do we need to remove a purchased item from products table?

        elif command == "feedback":

            # TODO: set counter for number of times reviewed
            # if this number is nonzero (1), do not allow review
            # else, submit review and increment n times reviewed
            
            item_id = tokens[1]
            review = tokens[2]
            u_id = tokens[3]
            if(int(u_id) == -1):
                data = "User is not logged in."
            else:

                pre_query = "SELECT s_id FROM product.products "\
                            + "INNER JOIN customer.purchased " \
                            + "ON products.id = customer.purchased.id " \
                            + "WHERE customer.purchased.b_id = " + u_id \
                            + " AND customer.purchased.id = " + item_id + ";"

                db_cursor.execute(pre_query)

                # get seller ID
                s_id = -1
                for x in db_cursor:
                    if(isinstance(x[0], int)):
                        s_id = x[0]

                if(s_id == -1):
                    data = "Error: seller not found or product not in purchase history."
                else:
                    # positive review
                    if(review == "True"):
                        sql_query = "UPDATE feedback SET pos=pos+1 WHERE id=" + str(s_id) + ";"
                    # negative review
                    else:
                        sql_query = "UPDATE feedback SET neg=neg+1 WHERE id=" + str(s_id) + ";"

                    cus_cursor.execute(sql_query)
                    cus_db.commit()

                    data = "Feedback given."

        elif command == "rating":
            # Writeup says to provide BUYER id, but I assume it means SELLER id
            s_id = tokens[1]
            sql_query = "SELECT pos, neg FROM feedback where id=" + s_id + ";"
            cus_cursor.execute(sql_query)

            for x in cus_cursor:
                data += str(x) + "\n"

            if(len(data) == 0):
                data = "Seller not found."

        elif command == "history":
            u_id = tokens[1]
            if(int(u_id) == -1):
                data = "User is not logged in."
            else:
                sql_query = "SELECT * FROM purchased WHERE b_id=" + u_id + ";"
                cus_cursor.execute(sql_query)

                for x in cus_cursor:
                    data += str(x) + "\n"

                if(len(data) == 0):
                    data="User has no purchase history."

                cus_db.commit()


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
