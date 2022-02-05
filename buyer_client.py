import sys
import socket
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8090

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, SERVER_PORT))

    print("--------Commands--------")
    print("1. search - search items for sale")
    print("2. add - add item to cart")
    print("3. remove - remove an item from the cart")
    print("4. clear - clear shopping cart")
    print("5. display - display shopping cart")

    while True:
        message = input("> ")

        if(message == "search"):
            search_category = input("Please enter search category: ")
            search_keywords = input("Please enter up to five keywords: ")
            message = "search\n" + search_category + "\n" + search_keywords

        elif(message == "add"):
            item_id = input("Please enter an item ID: ")
            item_quantity = input("Please enter an item quantity: ")
            message = "add\n" + item_id + "\n" + item_quantity

        elif(message == "remove"):
            item_id = input("Please enter an item ID: ")
            item_quantity = input("Please enter an item quantity: ")
            message = "remove\n" + item_id + "\n" + item_quantity

        elif(message == "clear"):
            message = "clear"

        elif(message == "display"):
            message = "display"

        else:
            print("Please enter a valid message.")
            continue

        time_1 = time.time()
        s.sendall(message.encode("utf-8"))
        data = s.recv(1024)
        time_2 = time.time()
        print(data.decode('utf-8'))
        print("(Took " + str(time_2-time_1) + " seconds)")
