import sys
import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8090

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT))

        while True:
            message = input("> ")

            if(len(message) == 0):
                print("Please enter a message.")
                continue

            s.sendall(message.encode("utf-8"))
            data = s.recv(1024)
            print('Received', repr(data))
