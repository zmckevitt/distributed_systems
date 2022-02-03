import sys
import socket
#import mysql.connector

HOST_IP = "127.0.0.1"

if __name__ == "__main__":

    if(len(sys.argv) < 2):
        print("Usage: %s <port>" % sys.argv[0])
        exit()

    PORT = int(sys.argv[1])

    # initialize socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST_IP, PORT))
    
    while True:
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                print("Data = ", data)
                if not data:
                    break
                conn.sendall(data)
