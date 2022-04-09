from concurrent import futures
import time
import grpc
import mysql.connector
import sys
import socket
import random

import marketplace_pb2_grpc as service
import marketplace_pb2 as message
import pymongo

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
server_list = ["10.128.0.4", "10.128.0.5", "10.128.0.6", "10.128.0.7", "10.128.0.8"]

myclient = pymongo.MongoClient("mongodb://mongoAdmin:Abstract09@localhost:27017")
my_mongo_db = myclient["product"]
dblist = myclient.list_database_names()
if "product" in dblist:
    print("Found database")
else:
    print("Database not found")

# prod_db = mysql.connector.connect(
#     host="10.180.0.6",
#     #host="127.0.0.1",
#     user="prod",
#     password="prodpassword",
#     database="product"
# )

# cus_db = mysql.connector.connect(
#     host="10.180.0.5",
#     #host="127.0.0.1",
#     user="prod",
#     password="prodpassword",
#     database="customer"
# )

# set up sockets
# send query to database group
# return result of query
def pass_query(query):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # choose random server to send to
    s.sendto(query.encode(), (server_list[random.randint(0,len(server_list)-1)], 8000))
    resp, addr = s.recvfrom(1024)
    return resp

class SellerService(service.marketplaceServicer):

    def sell(self, request, context):
        # Mongo implementation
        products = my_mongo_db.get_collection("products")
        data = ""
        if request.u_id == -1:
            data = "User is not logged in."
        else:
            max_row = products.find_one(sort=[("id", pymongo.DESCENDING)])
            max_id = 0
            if max_row is not None:
                max_id = max_row.get("id")
            print(max_id)

            new_id=max_id+1
            rows = products.insert_one(
                {"name": request.name, "category": request.category, "id": new_id, "keywords": request.keywords,
                 "price": request.price, "s_id": request.u_id})
            data = "Item listed successfully."
        ret = message.Response(text=data)

        """
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
        print(ret)  """
        return ret

    def modify(self, request, context):
        # Mongo implementation
        products = my_mongo_db.get_collection("products")
        data = ""
        if request.u_id == -1:
            data = "User is not logged in."
        else:
            products.update_one({"id": request.id, "s_id": request.u_id}, {"$set": {"price": request.price}})
            data = "Price updated successfully."
        ret = message.Response(text=data)

        """
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
        print(ret)  """
        return ret

    def removeListing(self, request, context):
        # Mongo implementation
        products = my_mongo_db.get_collection("products")
        data = ""
        if request.u_id == -1:
            data = "User is not logged in."
        else:
            for i in range(request.quantity):
                products.delete_one({"id": request.id, "s_id": request.u_id})
            data = "Entry removed."
        ret = message.Response(text=data)

        """
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
        print(ret)  """
        return ret

    def list(self, request, context):
        # Mongo implementation
        products = my_mongo_db.get_collection("products")
        rows = products.find({"s_id": request.u_id})
        data = ""
        for row in rows:
            data += str(row) + "\n"
        ret = message.Response(text=data)


        """
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
        print(ret)  """
        return ret

    def login(self, request, context):
        username = request.username
        password = request.password

        sql_query = "SELECT users.id FROM users " \
                    + "INNER JOIN passwords ON users.id=passwords.id " \
                    + "WHERE passwords.password = \"" + password + "\" " \
                    + "and users.name = \"" + username +"\";"

        data = pass_query(sql_query)
        print("received data:", data)

        # cus_cursor.execute(sql_query)

        # # get the returned user id
        # # u_id will be -1 if no matching user is found
        # u_id = -1
        # for x in cus_cursor:
        #     if(isinstance(x[0], int)):
        #         u_id = x[0]


        # # if user exists, set their status to logged in
        # if(u_id != -1):
        #     sql_query = "UPDATE logged SET logged=1 WHERE id=" + str(u_id) + ";"
        #     cus_cursor.execute(sql_query)

        # cus_db.commit()
        # data = str(u_id)

        ret = message.Response(text=data)
        return ret

    def logout(self, request, context):
        u_id = request.u_id
        if(u_id == -1):
            data = "User is not logged in."

        else:
            # sql_query = "UPDATE logged SET logged=0 WHERE id=" + str(u_id) + ";"
            # cus_cursor.execute(sql_query)
            # cus_db.commit()
            data = "Logged out."
        ret = message.Response(text=data)
        return ret

    def createUser(self, request, context):
        name = request.username
        password = request.password

        sql_query = "SELECT MAX(id) FROM customer.users;"
        data = pass_query(sql_query)
        print("received data:", data)

        # cus_cursor.execute("SELECT MAX(id) FROM customer.users;")
        # data = ""

        # new_id = 0
        # for x in cus_cursor:
        #     if(isinstance(x[0], int)):
        #         new_id = x[0]+1


        # sql_query = "INSERT INTO users " \
        #             + "(name, id, nitems) " \
        #             + "VALUES " \
        #             + "(\"" + name + "\", " + str(new_id) + ", " + "0);"

        # cus_cursor.execute(sql_query)

        # sql_query = "INSERT INTO passwords "\
        #             + "(id, password) " \
        #             + "VALUES " \
        #             + "(" + str(new_id) + ", " + "\"" + password + "\")"

        # cus_cursor.execute(sql_query)

        # sql_query = "INSERT INTO feedback "\
        #             + "(id, pos, neg) " \
        #             + "VALUES " \
        #             + "(" + str(new_id) + ", 0, 0);"

        # cus_cursor.execute(sql_query)


        # # logged table might be useless if we are using client side cookies to track login
        # sql_query = "INSERT INTO logged "\
        #             + "(id, logged) " \
        #             + "VALUES " \
        #             + "(" + str(new_id) + ", 0);"

        # cus_cursor.execute(sql_query)

        # data = "Customer added successfully."
        # cus_db.commit()

        ret = message.Response(text=data)
        return ret

    def rating(self, request, context):
        s_id = request.s_id        
        sql_query = "SELECT pos, neg FROM feedback where id=" + str(s_id) + ";"
        # cus_cursor.execute(sql_query)

        # data = ""
        # for x in cus_cursor:
        #     data += str(x) + "\n"

        # if(len(data) == 0):
        #     data = "User not logged in"
        data = pass_query(sql_query)

        ret = message.Response(text=data)
        print(ret)
        return ret


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service.add_marketplaceServicer_to_server(SellerService(), server)
    server.add_insecure_port('10.180.0.7:8080')
    #server.add_insecure_port('127.0.0.1:8080')
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