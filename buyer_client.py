import sys
import socket
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8090

# REST API allows for cookies when stored client side
# cookie required to maintain login state
# keep track of seller ID
# initialize to -1 to represent logged out
COOKIE_ID = -1

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, SERVER_PORT))

    print("--------Commands--------")
    print("1. search - search items for sale")
    print("2. add - add item to cart")
    print("3. remove - remove an item from the cart")
    print("4. clear - clear shopping cart")
    print("5. display - display shopping cart")
    print("5. create - create user by setting username and password")
    print("6. login - login with username and password")
    print("7. logout")
    print("8. purchase - make a purchase")
    print("9. feedback - give feedback for a seller")
    print("10. rating - see seller rating")
    print("11. history - get buyer history (must be logged in)")

    while True:
        set_cookie = False
        message = input("> ")

        if(message == "search"):
            search_category = input("Please enter search category: ")
            search_keywords = input("Please enter up to five keywords: ")
            message = "search\n" + search_category + "\n" + search_keywords

        elif(message == "add"):
            item_id = input("Please enter an item ID: ")
            item_quantity = input("Please enter an item quantity: ")
            message = "add\n" + item_id + "\n" + item_quantity + "\n" + str(COOKIE_ID)

        elif(message == "remove"):
            item_id = input("Please enter an item ID: ")
            item_quantity = input("Please enter an item quantity: ")
            message = "remove\n" + item_id + "\n" + item_quantity + "\n" + str(COOKIE_ID)

        elif(message == "clear"):
            message = "clear\n" + str(COOKIE_ID)

        elif(message == "display"):
            message = "display\n" + str(COOKIE_ID)

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

        elif(message == "purchase"):

            name = input("Enter name on card: ")
            number = input("Enter card number: ")
            expiration = input("Enter card expiration: ")

            message = "purchase\n" + name + "\n" + number + "\n" \
                    + expiration + "\n" + str(COOKIE_ID)

        elif(message == "feedback"):

            item_id = input("Please provide an ID for an item you've purchased: ")
            item_review = input("Was the item (good) or (bad)? ")

            if(item_review.lower() == "good" ):
                item_review = "True"
            else:
                item_review = "False"

            message = "feedback\n" + item_id + "\n" + item_review + "\n" + str(COOKIE_ID)

        elif(message == "rating"):

            # Writeup says to provide BUYER id, but I assume it means SELLER id
            s_id = input("Please provide a seller ID: ")
            message = "rating\n" + s_id + "\n" + str(COOKIE_ID)

        elif(message == "history"):
            message = "history\n" + str(COOKIE_ID)

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
