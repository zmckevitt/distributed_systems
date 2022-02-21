from concurrent import futures
import time
import grpc
import mysql.connector
import sys

import marketplace_pb2_grpc as service
import marketplace_pb2 as message

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

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


class BuyerService(service.marketplaceServicer):
    def Search(self, request, context):
        sql_query = "SELECT * FROM products " \
                    "WHERE category = " + request.category + " AND keywords LIKE '%" + request.keywords + "%';"
        print(sql_query)
        db_cursor.execute(sql_query)
        result = db_cursor.fetchall()
        data = ""
        for x in result:
            data += str(x) + "\n"
        if len(data) == 0:
            data = "No matching data found."
        print(data)
        return data

    def add(self, request, context):
        print("u_id = ", request.u_id )
        if (request.u_id == -1):
            data = "User is not logged in."
            print("User is not logged in.")
        else:
            print("in handler...")
            pre_query = "SELECT id FROM cart WHERE id = " + request.item_id + " AND b_id=" + request.u_id + ";"
            db_cursor.execute(pre_query)
            if db_cursor.rowcount == 0:
                sql_query = "INSERT INTO cart VALUES(" + request.item_id + "," + request.u_id + "," + request.quantity + ");"
                new_cursor = prod_db.cursor()
                new_cursor.execute(sql_query)
                if new_cursor.rowcount > 0:
                    data = "Item added successfully."
                else:
                    data = "Item could not be added"
            else:
                sql_query = "UPDATE cart SET quantity = quantity+" + request.quantity \
                            + " WHERE id = " + request.item_id + " AND b_id=" + request.u_id + ";"
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
            return ret

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service.add_marketplaceServicer_to_server(BuyerService(), server)
    server.add_insecure_port('127.0.0.1:8090')
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
    #cus_cursor = cus_db.cursor(buffered=True)
    serve()