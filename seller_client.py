import sys
import socket
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080

# REST API allows for cookies when stored client side
# cookie required to maintain login state
# keep track of seller ID
# initialize to -1 to represent logged out
COOKIE_ID = -1

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, SERVER_PORT))

    print("--------Commands--------")
    print("1. sell - list an item for sale")
    print("2. modify - change sale price of an item")
    print("3. remove - remove a listed item")
    print("4. list - list all items for sale by seller")
    print("5. create - create user by setting username and password")
    print("6. login - login with username and password")
    print("7. logout")
    print("8. rating - get your seller rating (must be logged in)")

    while True:
        set_cookie = False
        message = input("> ")            

        if(message == "sell"):
            item_name = input("Please enter an item name: ")
            item_category = input("Please enter an item category: ")
            item_keywords = input("Please enter item keywords: ")
            item_condition = input("Please enter the item's condition: ")
            if(item_condition.lower() == "new" ):
                item_condition = "True"
            else:
                item_condition = "False"
            item_price = input("Please enter the price of the item: ")
            message = "sell\n" + item_name + "\n" + item_category + "\n" + item_keywords \
                    + "\n" + item_condition + "\n" + item_price + "\n" + str(COOKIE_ID)

        elif(message == "modify"):
            item_id = input("Please enter the item ID: ")
            item_price = input("Please list the new price: ")
            message = "modify\n" + item_id + "\n" + item_price + "\n" + str(COOKIE_ID)

        elif(message == "remove"):
            item_id = input("Please enter the item ID: ")
            item_quantity = input("Please enter the quantity: ")
            message = "remove\n" + item_id + "\n" + item_quantity

        elif(message == "list"):
            message = "list\n" + str(COOKIE_ID)

        elif(message == "create"):
            username = input("Enter a username: ")
            password = input("Enter a password: ")

            message = "create\n" + username + "\n" + password

        elif(message == "login"):
            
            # will need to set COOKIE_ID from response
            set_cookie = True

            username = input("Enter a username: ")
            password = input("Enter a password: ")

            message = "login\n" + username + "\n" + password

        elif(message == "logout"):
            message = "logout\n" + str(COOKIE_ID)
            COOKIE_ID = -1

        elif(message == "rating"):

            # send COOKIE_ID along with rating
            message = "rating\n" + str(COOKIE_ID)

        else:
            print("Please enter a valid message.")
            continue

        time_1 = time.time()
        s.sendall(message.encode("utf-8"))
        data = s.recv(1024)
        time_2 = time.time()
        data = data.decode('utf-8')

        if(set_cookie):
            COOKIE_ID = int(data)
            if(COOKIE_ID != -1):
                print("Logged in with UID: " + str(COOKIE_ID))
            else:
                print("Invalid username or password.")

        else:
            print(data)

        print("(Took " + str(time_2-time_1) + " seconds)")
