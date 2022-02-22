from concurrent import futures
import time
import grpc
import mysql.connector
import sys

import marketplace_pb2_grpc as service
import marketplace_pb2 as message

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

prod_db = mysql.connector.connect(
    host="10.180.0.6",
    user="prod",
    password="prodpassword",
    database="product"
)

cus_db = mysql.connector.connect(
    host="10.180.0.5",
    user="prod",
    password="prodpassword",
    database="customer"
)

class SellerService(service.marketplaceServicer):

    def sell(self, request, context):
        item_name = request.name
        item_category = request.category
        item_keywords = request.keywords
        item_condition = request.condition
        item_price = request.price
        u_id = request.u_id
        if(u_id == -1):
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
                        + "(\"" + item_name + "\", " + str(item_category) + ", " \
                        + str(new_id) + ", " + "\"" + item_keywords + "\", " \
                        + str(item_condition) + ", " + str(item_price) + ", " + str(u_id) + ");"

            print(sql_query)
            db_cursor.execute(sql_query)
            data = "Item listed successfully."
            prod_db.commit()

        ret = message.Response(text=data)
        print(ret)
        return ret

    def modify(self, request, context):
        item_id = request.id
        new_price = request.price
        u_id = request.u_id

        if(u_id == -1):
            data = "User is not logged in."
            
        else:
            sql_query = "UPDATE products SET price=" + str(new_price) + " WHERE id=" + str(item_id) + " AND s_id=" + str(u_id) + ";"
            db_cursor.execute(sql_query)
            data = "Price updated successfully."
            prod_db.commit()

        ret = message.Response(text=data)
        print(ret)
        return ret

    def removeListing(self, request, context):
        item_id = request.id
        item_quantity = request.quantity
        u_id = request.u_id

        if(u_id == -1):
            data = "User is not logged in."

        else:
            sql_query = "DELETE FROM products WHERE id=" + str(item_id) + " AND s_id=" + str(u_id) + " LIMIT " + str(item_quantity) + ";"
            db_cursor.execute(sql_query)
            data = "Entry removed."
            prod_db.commit()

        ret = message.Response(text=data)
        print(ret)
        return ret

    def list(self, request, context):
        u_id = request.u_id
        if(u_id == -1):
            data = "User is not logged in."

        else:
            db_cursor.execute("SELECT * FROM products WHERE s_id=" + str(u_id) + ";")
            data = ""
            for x in db_cursor:
                data += str(x) + "\n"
            if(len(data) == 0):
                data = "Database is empty."

        ret = message.Response(text=data)
        print(ret)
        return ret

    def login(self, request, context):
        username = request.username
        password = request.password

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

        ret = message.Response(text=data)
        return ret

    def logout(self, request, context):
        u_id = request.u_id
        if(u_id == -1):
            data = "User is not logged in."

        else:
            sql_query = "UPDATE logged SET logged=0 WHERE id=" + str(u_id) + ";"
            cus_cursor.execute(sql_query)
            cus_db.commit()
            data = "Logged out."
        ret = message.Response(text=data)
        return ret

    def createUser(self, request, context):
        name = request.username
        password = request.password

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

        ret = message.Response(text=data)
        return ret

    def rating(self, request, context):
        s_id = request.s_id        
        sql_query = "SELECT pos, neg FROM feedback where id=" + str(s_id) + ";"
        cus_cursor.execute(sql_query)

        data = ""
        for x in cus_cursor:
            data += str(x) + "\n"

        if(len(data) == 0):
            data = "User not logged in"

        ret = message.Response(text=data)
        print(ret)
        return ret


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service.add_marketplaceServicer_to_server(SellerService(), server)
    server.add_insecure_port('10.180.0.7:8080')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print('Srever Stop')
        server.stop(0)
    #server.wait_for_termination()


if __name__ == "__main__":
    print('DB Server Start')
    db_cursor = prod_db.cursor(buffered=True)
    cus_cursor = cus_db.cursor(buffered=True)
    serve()