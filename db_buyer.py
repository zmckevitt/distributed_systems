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
from pymongo import MongoClient
c = MongoClient()

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

#myclient = pymongo.MongoClient("mongodb://mongoAdmin:Abstract09@localhost:27017")
#myclient = pymongo.MongoClient("mongodb://34.106.188.170:27017, 34.106.139.133:27017, 34.106.31.27 :27017, 34.106.9.186:27017")
myclient = pymongo.MongoClient("mongodb://10.180.0.14:27017, 10.180.0.13:27017, 10.180.0.12:27017, 10.180.0.11:27017, 10.180.0.10:27017")

server_list = ["10.128.0.4", "10.128.0.5", "10.128.0.6", "10.128.0.7", "10.128.0.8"]
dblist = myclient.list_database_names()
if "product" in dblist:
    print("Found database")
else:
    print("Database not found. Creating...")
    db = c['product']
my_mongo_db = myclient["product"]

"""prod_db = mysql.connector.connect(
    host="10.180.0.6",
    #host="127.0.0.1",
    user="prod",
    password="prodpassword",
    database="product"
)   """

cus_db = mysql.connector.connect(
    host="10.180.0.5",
    #host="127.0.0.1",
    user="prod",
    password="prodpassword",
    database="customer"
)

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
    return resp.decode()

class BuyerService(service.marketplaceServicer):
    def search(self, request, context):
        #Mongo implementation
        products = my_mongo_db.get_collection("products")
        rows = products.find({ "category": request.category, "keywords" : request.keywords})
        data = ""
        for row in rows:
            data += str(row) + "\n"
        ret = message.Response(text=data)

        #MySQL implementation
        """sql_query = "SELECT * FROM products " \
                    "WHERE category = " + str(request.category) + " AND keywords LIKE '%" + request.keywords + "%';"
        print(sql_query)
        db_cursor.execute(sql_query)
        # result = db_cursor.fetchall()
        data = ""
        for x in db_cursor:
            data += str(x) + "\n"
        if len(data) == 0:
            data = "No matching data found."
        prod_db.commit()
        ret = message.Response(text=data)
        print(ret) """
        return ret

    # ISSUE: can add items not listed for sale to cart
    # FIX: sql joins
    def add(self, request, context):
        # Mongo implementation
        cart = my_mongo_db.get_collection("cart")
        data = ""
        if request.u_id == -1:
            data = "User is not logged in."
        else:
            print("User already logged...")
            rows = cart.find({ "item_id": request.item_id, "b_id" : request.u_id})
            count = 0
            for row in rows:
                count +=1
            if count == 0:
                inserted = cart.insert_one({"item_id": request.item_id, "b_id": request.u_id, "quantity": request.quantity})
                inserted_count=1
                if inserted_count>0:
                    data = "Item added successfully."
                else:
                    data = "Item could not be added"
            else:
                update_count = cart.update_one({"item_id":request.item_id, "b_id": request.u_id}, {"$set":{"quantity": request.quantity}})
                update_count=1
                if update_count > 0:
                    data = "Item added successfully."
                else:
                    data = "Item could not be added"
        ret = message.Response(text=data)

        """
        print("u_id = ", request.u_id )
        if (request.u_id == -1):
            data = "User is not logged in."
        else:
            print("in handler...")
            pre_query = "SELECT id FROM cart WHERE id = " + str(request.item_id) + " AND b_id=" + str(request.u_id) + ";"
            db_cursor.execute(pre_query)
            if db_cursor.rowcount == 0:
                sql_query = "INSERT INTO cart VALUES(" + str(request.item_id) + "," + str(request.u_id) + "," + str(request.quantity) + ");"
                new_cursor = prod_db.cursor()
                new_cursor.execute(sql_query)
                if new_cursor.rowcount > 0:
                    data = "Item added successfully."
                else:
                    data = "Item could not be added"
            else:
                sql_query = "UPDATE cart SET quantity = quantity+" + str(request.quantity) \
                            + " WHERE id = " + str(request.item_id) + " AND b_id=" + str(request.u_id) + ";"
                print(sql_query)
                new_cursor = prod_db.cursor()
                new_cursor.execute(sql_query)
                if new_cursor.rowcount > 0:
                    data = "Item added successfully."
                else:
                    data = "Item could not be added"
            prod_db.commit()
            print("commited query")
        ret = message.Response(text=data)
        print(ret) """
        return ret

    def remove(self, request, context):
        #Mongo implementation
        cart = my_mongo_db.get_collection("cart")
        data = ""
        row = cart.find_one({"item_id": request.item_id, "b_id": request.u_id})
        curr_quantity = row.get('quantity')
        updated = cart.update_one({"item_id": request.item_id, "quantity": {"$gte":request.quantity}}, {"$set": {"quantity": curr_quantity-request.quantity}})
        update_count=1
        if update_count>0:
            data = "Item(s) removed successfully."
        else:
            data = "Item(s) could not be removed"
        ret = message.Response(text=data)
        """
        item_id = request.item_id
        item_quantity = request.quantity
        u_id = request.u_id

        if(u_id == -1):
            data = "User is not logged in."

        else:
            sql_query = "UPDATE cart SET quantity = quantity-" + str(item_quantity) \
                        + " WHERE id = " + str(item_id) + " AND quantity-" \
                        + str(item_quantity) + ">=0" + " AND b_id=" + str(u_id) + ";"
            print(sql_query)
            db_cursor.execute(sql_query)
            prod_db.commit()
            if db_cursor.rowcount > 0:
                data = "Item(s) removed successfully."
            else:
                data = "Item(s) could not be removed"

        ret = message.Response(text=data)
        print(ret)  """
        return ret

    def clear(self, request, context):
        # Mongo implementation
        cart = my_mongo_db.get_collection("cart")
        data = ""
        deleted = cart.delete_many({"b_id": request.u_id})
        del_count=1
        if del_count>0:
            data = "Cart cleared successfully."
        else:
            data = "Cart could not be cleared"
        ret = message.Response(text=data)

        """
        u_id = request.u_id
        if(u_id == -1):
            data = "User is not logged in."

        else:
            sql_query = "DELETE FROM cart WHERE b_id=" + str(u_id) + ";"
            print(sql_query)
            db_cursor.execute(sql_query)
            prod_db.commit()
            if db_cursor.rowcount > 0:
                data = "Cart cleared successfully."
            else:
                data = "Cart could not be cleared"

        ret = message.Response(text=data)
        print(ret)  """
        return ret

    def display(self, request, context):
        # Mongo implementation
        cart = my_mongo_db.get_collection("cart")
        rows = cart.find({"b_id":request.u_id})
        data = ""
        for row in rows:
            data += str(row) + "\n"
        ret = message.Response(text=data)

        """
        u_id = request.u_id
        if(u_id == -1):
            data = "User is not logged in."

        else:
            sql_query = "SELECT * FROM cart WHERE b_id=" + str(u_id) + ";"
            db_cursor.execute(sql_query)
            result = db_cursor.fetchall()
            data = ""
            for x in result:
                data += str(x) + "\n"
            if len(data) == 0:
                data = "Your cart is empty."
            print(data)

        ret = message.Response(text=data)
        print(ret)  """
        return ret

    def feedback(self, request, context):
        # item_id = request.item_id
        # review = request.item_review
        # u_id = request.u_id
        
        # if(u_id == -1):
        #     data = "User is not logged in."
        # else:

        #     pre_query = "SELECT id FROM purchased WHERE id=" + str(item_id) + " AND b_id=" + str(u_id) + ";"
        #     cus_cursor.execute(pre_query)

        #     # get seller ID
        #     i_id = -1
        #     for x in cus_cursor:
        #         if(isinstance(x[0], int)):
        #             i_id = x[0]

        #     if(i_id == -1):
        #         data = "Error: seller not found or product not in purchase history."
        #     else:

        #         pre_query = "SELECT s_id FROM products WHERE id=" + str(i_id) + ";"

        #         db_cursor.execute(pre_query)

        #         s_id = -1
        #         for x in db_cursor:
        #             if(isinstance(x[0], int)):
        #                 s_id = x[0]

        #         if(s_id == -1):
        #             data = "Error: seller not found or product not in purchase history."

        #         else:
        #             # positive review
        #             if(review == "True"):
        #                 sql_query = "UPDATE feedback SET pos=pos+1 WHERE id=" + str(s_id) + ";"
        #             # negative review
        #             else:
        #                 sql_query = "UPDATE feedback SET neg=neg+1 WHERE id=" + str(s_id) + ";"

        #         cus_cursor.execute(sql_query)
        #         cus_db.commit()

        #         data = "Feedback given."
        # data = pass_query("DEFAULT\n"+"feedback")
        data = "Feedback given."
        ret = message.Response(text=data)
        print(ret)
        return ret

    def rating(self, request, context):
        s_id = request.s_id        
        sql_query = "SELECT pos, neg FROM feedback where id=" + str(s_id) + ";"
        # cus_cursor.execute(sql_query)

        # data = ""
        # for x in cus_cursor:
        #     data += str(x) + "\n"

        # if(len(data) == 0):
        #     data = "Seller not found."
        data = pass_query("DEFAULT\n"+sql_query)
        ret = message.Response(text=data)
        print(ret)
        return ret

    def history(self, request, context):
        u_id = request.u_id
        if(u_id == -1):
            data = "User is not logged in."
        else:
            sql_query = "SELECT * FROM customer.purchased WHERE b_id=" + str(u_id) + ";"
            # cus_cursor.execute(sql_query)

            # data = ""
            # for x in cus_cursor:
            #     data += str(x) + "\n"

            # if(len(data) == 0):
            #     data="User has no purchase history."

            # cus_db.commit()
            data = pass_query("DEFAULT\n"+sql_query)
        ret = message.Response(text=data)
        print(ret)
        return ret

    def purchase(self, request, context):
        name = request.name
        number = request.number
        expiration = request.expiration
        u_id = request.u_id

        if(u_id == -1):
            data = "User is not logged in."

        else:

            # send purchase request to third party

            # if invalid, exit

            # if valid, add item to purchase table FROM CART
            pre_query = "SELECT id, b_id, quantity FROM product.cart WHERE product.cart.b_id=" + str(u_id) + ";"

            db_cursor.execute(pre_query)

            for row in db_cursor:
                try:
                    _id = row[0]
                    b_id = row[1]
                    quantity = row[2]
                    sql_query = "INSERT INTO customer.purchased (id, b_id, quantity) " \
                            + "VALUES (" + str(_id) + ", " + str(b_id) + ", " + str(quantity) + ");"

                    cus_cursor.execute(sql_query)
                    cus_db.commit()
                    print(_id)
                    print(b_id)
                    print(quantity)
                except:
                    break


            # clear cart
            sql_query = "DELETE FROM product.cart WHERE b_id=" + str(u_id) + ";"

            db_cursor.execute(sql_query)

            prod_db.commit()
            data = "Items have been purchased!"

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
        data = pass_query("LOGIN\n"+sql_query)
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
        data = pass_query("CREATE\n"+sql_query)
        print("received data:", data)

        # cus_cursor.execute("SELECT MAX(id) FROM customer.users;")
        # data = ""

        # new_id = 0
        # for x in cus_cursor:
        #     if(isinstance(x[0], int)):
        #         new_id = x[0]+1


        sql_query = "INSERT INTO users " \
                    + "(name, id, nitems) " \
                    + "VALUES " \
                    + "(\"" + name + "\", " + data + ", " + "0);"

        _ = pass_query("DISCARD\n" + sql_query)

        # cus_cursor.execute(sql_query)

        sql_query = "INSERT INTO passwords "\
                    + "(id, password) " \
                    + "VALUES " \
                    + "(" + data+ ", " + "\"" + password + "\")"

        _ = pass_query("DISCARD\n" + sql_query)

        # cus_cursor.execute(sql_query)

        sql_query = "INSERT INTO feedback "\
                    + "(id, pos, neg) " \
                    + "VALUES " \
                    + "(" + data + ", 0, 0);"

        _ = pass_query("DISCARD\n" + sql_query)

        # cus_cursor.execute(sql_query)


        # # logged table might be useless if we are using client side cookies to track login
        # sql_query = "INSERT INTO logged "\
        #             + "(id, logged) " \
        #             + "VALUES " \
        #             + "(" + str(new_id) + ", 0);"

        # cus_cursor.execute(sql_query)

        data = "Customer added successfully."
        # cus_db.commit()
        ret = message.Response(text=data)
        return ret


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service.add_marketplaceServicer_to_server(BuyerService(), server)
    server.add_insecure_port('10.180.0.4:8090')
    #server.add_insecure_port('127.0.0.1:8090')
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
    #db_cursor = prod_db.cursor(buffered=True)
    #cus_cursor = cus_db.cursor(buffered=True)
    serve()
