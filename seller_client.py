import sys
import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, SERVER_PORT))

    print("--------Commands--------")
    print("1. sell - list an item for sale")
    print("2. modify - change sale price of an item")
    print("3. remove - remove a listed item")
    print("4. list - list all items for sale by seller")

    while True:
        message = input("> ")            

        if(message == "sell"):
            item_name = input("Please enter an item name: ")
            item_category = input("Please enter an item category: ")
            item_id = input("Please enter an item ID: ")
            item_keywords = input("Please enter item keywords: ")
            item_condition = input("Please enter the item's condition: ")
            if(item_condition.lower() == "new" ):
                item_condition = "True"
            else:
                item_condition = "False"
            item_price = input("Please enter the price of the item: ")
            message = "sell\n" + item_name + "\n" + item_category + "\n" + item_id \
                    + "\n" + item_keywords + "\n" + item_condition + "\n" + item_price

        elif(message == "modify"):
            item_id = input("Please enter the item ID: ")
            item_price = input("Please list the new price: ")
            message = "modify\n" + item_id + "\n" + item_price

        elif(message == "remove"):
            item_id = input("Please enter the item ID: ")
            item_quantity = input("Please enter the quantity: ")
            message = "remove\n" + item_id + "\n" + item_quantity

        elif(message == "list"):
            message = "list"

        else:
            print("Please enter a valid message.")
            continue

        s.sendall(message.encode("utf-8"))
        data = s.recv(1024)
        print(data.decode('utf-8'))
