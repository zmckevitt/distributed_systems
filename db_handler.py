from concurrent import futures
import time
import grpc
import mysql.connector
import sys
#import pymysql
#from config import conn

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
    conn.close()