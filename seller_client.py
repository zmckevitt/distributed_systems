import sys
import time
import requests as reqs

#SERVER_IP = "http://127.0.0.1"
SERVER_IP = "http://34.106.188.170"
SERVER_PORT = "5000"
BASE_URL = SERVER_IP+":"+SERVER_PORT

# REST API allows for cookies when stored client side
# cookie required to maintain login state
# keep track of seller ID
# initialize to -1 to represent logged out
COOKIE_ID = -1

if __name__ == "__main__":

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
                    "u_id": COOKIE_ID}
            url = BASE_URL+"/products/sell"
            time_1 = time.time()
            response = reqs.post(url, data)
            time_2 = time.time()
            print(response.status_code)
            print(response.text)
            print("(Took " + str(time_2-time_1) + " seconds)")

        elif(message == "modify"):
            item_id = input("Please enter the item ID: ")
            item_price = input("Please list the new price: ")

            data = {"id": item_id,
                    "price": item_price,
                    "u_id": COOKIE_ID}
            url = BASE_URL+"/products/modify"
            time_1 = time.time()
            response = reqs.post(url, data)
            time_2 = time.time()
            print(response.status_code)
            print(response.text)
            print("(Took " + str(time_2-time_1) + " seconds)")

        elif(message == "remove"):
            item_id = input("Please enter the item ID: ")
            item_quantity = input("Please enter the quantity: ")

            data = {"id": item_id,
                    "quantity": item_quantity,
                    "u_id": COOKIE_ID}
            url = BASE_URL+"/products/remove"
            time_1 = time.time()
            response = reqs.post(url, data)
            time_2 = time.time()
            print(response.status_code)
            print(response.text)
            print("(Took " + str(time_2-time_1) + " seconds)")

        elif(message == "list"):
            data = {"u_id": COOKIE_ID}
            url = BASE_URL+"/products/list"
            time_1 = time.time()
            response = reqs.post(url, data)
            time_2 = time.time()
            print(response.status_code)
            print(response.text)
            print("(Took " + str(time_2-time_1) + " seconds)")

        elif(message == "create"):
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            data = {"username": username, "password": password}
            url = BASE_URL+"/user/createUser"
            time_1 = time.time()
            response = reqs.post(url, data)
            time_2 = time.time()
            print(response.status_code)
            print(response.text)
            print("(Took " + str(time_2-time_1) + " seconds)")

        elif(message == "login"):

            username = input("Enter a username: ")
            password = input("Enter a password: ")
            data = {"username": username, "password": password}
            url = BASE_URL+"/user/login"
            time_1 = time.time()
            response = reqs.post(url, data)
            time_2 = time.time()
            print(response.status_code)
            print(response.text)
            print("(Took " + str(time_2-time_1) + " seconds)")

            COOKIE_ID = int(response.text[7:-2])
            if(COOKIE_ID != -1):
                print("Logged in with u_id: " + str(COOKIE_ID))
            else:
                print("Login failed.")

        elif(message == "logout"):
            data = {"u_id": COOKIE_ID}
            url = BASE_URL+"/user/logout"
            time_1 = time.time()
            response = reqs.post(url, data)
            time_2 = time.time()
            print(response.status_code)
            print(response.text)
            print("(Took " + str(time_2-time_1) + " seconds)")
            COOKIE_ID = -1

        elif (message == "rating"):

            data = {"s_id": COOKIE_ID}
            url = BASE_URL+"/rating"
            time_1 = time.time()
            response = reqs.post(url, data)
            time_2 = time.time()
            print(response.status_code)
            print(response.text)
            print("(Took " + str(time_2-time_1) + " seconds)")

        else:
            print("Please enter a valid message.")
            continue