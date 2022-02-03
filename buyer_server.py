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

        if(command == "search"):
            pass
        elif(command == "add"):
            pass
        elif(command == "remove"):
            pass
        elif(command == "clear"):
            pass
        elif(command == "display"):
            pass
        else:
            data = "ERROR"

        data = "hello"
        
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
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                print("Data = ", data)
                if not data:
                    break
                conn.sendall(data)
        print('Connected by', addr)
        start_new_thread(thread_handler, (conn,))
    s.close()        
