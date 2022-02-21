import sys
import time
import requests as reqs

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080

# REST API allows for cookies when stored client side
# cookie required to maintain login state
# keep track of seller ID
# initialize to -1 to represent logged out
COOKIE_ID = -1

if __name__ == "__main__":
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect((SERVER_IP, SERVER_PORT))

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

            data = {"name": item_name,
                    "category": item_category,
                    "keywords" : item_keywords,
                    "condition": item_condition,
                    "price" : item_price,
                    "cookie": str(COOKIE_ID)}
            url = "http://localhost:5000/products/sell"
            response = reqs.post(url, data)
            print(response.status_code)
            print(response.text)

        elif(message == "modify"):
            item_id = input("Please enter the item ID: ")
            item_price = input("Please list the new price: ")

            data = {"id": item_id,
                    "price": item_price,
                    "cookie": str(COOKIE_ID)}
            url = "http://localhost:5000/products/modify"
            response = reqs.post(url, data)
            print(response.status_code)
            print(response.text)

        elif(message == "remove"):
            item_id = input("Please enter the item ID: ")
            item_quantity = input("Please enter the quantity: ")

            data = {"id": item_id,
                    "quantity": item_quantity,
                    "cookie": str(COOKIE_ID)}
            url = "http://localhost:5000/products/remove"
            response = reqs.post(url, data)
            print(response.status_code)
            print(response.text)

        elif(message == "list"):
            data = {"cookie": str(COOKIE_ID)}
            url = "http://localhost:5000/products/list"
            response = reqs.post(url, data)
            print(response.status_code)
            print(response.text)

        elif(message == "create"):
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            data = {"username": username, "password": password}
            url = "http://localhost:5000/user/createUser"
            response = reqs.post(url, data)
            print(response.status_code)
            print(response.text)

        elif(message == "login"):

            # will need to set COOKIE_ID from response
            set_cookie = True

            username = input("Enter a username: ")
            password = input("Enter a password: ")
            data = {"username": username, "password": password}
            url = "http://localhost:5000/user/login"
            response = reqs.post(url, data)
            print(response.status_code)
            print(response.text)

            # set cookie
            # COOKIE_ID = int(response.text)

        elif(message == "logout"):
            message = "logout\n" + str(COOKIE_ID)
            data = {"cookie": str(COOKIE_ID)}
            url = "http://localhost:5000/user/logout"
            response = reqs.post(url, data)
            print(response.status_code)
            print(response.text)
            COOKIE_ID = -1

        elif (message == "rating"):

            # Writeup says to provide BUYER id, but I assume it means SELLER id
            s_id = input("Please provide a seller ID: ")

            data = {"seller_id": s_id, "cookie": str(COOKIE_ID)}
            url = "http://localhost:5000/rating"
            response = reqs.post(url, data)
            print(response.status_code)
            print(response.text)

        else:
            print("Please enter a valid message.")
            continue

        # time_1 = time.time()
        # s.sendall(message.encode("utf-8"))
        # data = s.recv(1024)
        # time_2 = time.time()
        # data = data.decode('utf-8')

        # if(set_cookie):
        #     COOKIE_ID = int(data)
        #     if(COOKIE_ID != -1):
        #         print("Logged in with UID: " + str(COOKIE_ID))
        #     else:
        #         print("Invalid username or password.")

        # else:
        #     print(data)

        # print("(Took " + str(time_2-time_1) + " seconds)")
