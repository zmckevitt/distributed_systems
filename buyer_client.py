import sys
import time
import requests as reqs


#SERVER_IP = "http://127.0.0.1"
# SERVER_IP = "http://34.106.57.85"
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
        message = input("> ")

        if(message == "search"):
            search_category = input("Please enter search category: ")
            search_keywords = input("Please enter up to five keywords: ")
            data = {"category": int(search_category), "keywords":search_keywords}
            url = BASE_URL+"/cart/searchProduct"
            time_1 = time.time()
            response = reqs.post(url, data)
            time_2 = time.time()
            print(response.status_code)
            print(response.text)
            print("(Took " + str(time_2 - time_1) + " seconds)")

        elif(message == "add"):
            item_id = input("Please enter an item ID: ")
            item_quantity = input("Please enter an item quantity: ")
            data = {"item_id": item_id, "u_id": COOKIE_ID, "quantity": item_quantity}
            url = BASE_URL+"/cart/addItem"
            time_1 = time.time()
            response = reqs.post(url, data)
            time_2 = time.time()
            print(response.status_code)
            print(response.text)
            print("(Took " + str(time_2 - time_1) + " seconds)")

        elif(message == "remove"):
            item_id = input("Please enter an item ID: ")
            item_quantity = input("Please enter an item quantity: ")
            data = {"item_id": item_id, "u_id": COOKIE_ID, "quantity": item_quantity}
            url = BASE_URL+"/cart/removeItem"
            time_1 = time.time()
            response = reqs.post(url, data)
            time_2 = time.time()
            print(response.status_code)
            print(response.text)
            print("(Took " + str(time_2 - time_1) + " seconds)")

        elif(message == "clear"):
            data = {"u_id" : COOKIE_ID}
            url = BASE_URL+"/cart/clear"
            time_1 = time.time()
            response = reqs.post(url, data)
            time_2 = time.time()
            print(response.status_code)
            print(response.text)
            print("(Took " + str(time_2 - time_1) + " seconds)")

        elif(message == "display"):
            data = {"u_id" : COOKIE_ID}
            url = BASE_URL+"/cart/display"
            time_1 = time.time()
            response = reqs.post(url, data)
            time_2 = time.time()
            print(response.status_code)
            print(response.text)
            print("(Took " + str(time_2 - time_1) + " seconds)")

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
            print("(Took " + str(time_2 - time_1) + " seconds)")

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
            print("(Took " + str(time_2 - time_1) + " seconds)")

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
            print("(Took " + str(time_2 - time_1) + " seconds)")
            COOKIE_ID = -1

        elif (message == "purchase"):

            name = input("Enter name on card: ")
            number = input("Enter card number: ")
            expiration = input("Enter card expiration: ")

            data = {"name": name, "number": number, "expiration": expiration, 'u_id' : COOKIE_ID}
            url = BASE_URL+"/purchase"
            time_1 = time.time()
            response = reqs.post(url, data)
            time_2 = time.time()
            print(response.status_code)
            print(response.text)
            print("(Took " + str(time_2 - time_1) + " seconds)")

        elif (message == "feedback"):

            item_id = input("Please provide an ID for an item you've purchased: ")
            item_review = input("Was the item (good) or (bad)? ")

            if (item_review.lower() == "good"):
                item_review = "True"
            else:
                item_review = "False"

            data = {"item_id": item_id, "item_review": item_review, "u_id": COOKIE_ID}
            url = BASE_URL+"/feedback"
            time_1 = time.time()
            response = reqs.post(url, data)
            time_2 = time.time()
            print(response.status_code)
            print(response.text)
            print("(Took " + str(time_2 - time_1) + " seconds)")

        elif (message == "rating"):

            # Writeup says to provide BUYER id, but I assume it means SELLER id
            s_id = input("Please provide a seller ID: ")

            data = {"s_id": s_id}
            url = BASE_URL+"/rating"
            time_1 = time.time()
            response = reqs.post(url, data)
            time_2 = time.time()
            print(response.status_code)
            print(response.text)
            print("(Took " + str(time_2 - time_1) + " seconds)")

        elif (message == "history"):
            data = {"u_id": COOKIE_ID}
            url = BASE_URL+"/history"
            time_1 = time.time()
            response = reqs.post(url, data)
            time_2 = time.time()
            print(response.status_code)
            print(response.text)
            print("(Took " + str(time_2 - time_1) + " seconds)")

        else:
            print("Please enter a valid message.")
            continue