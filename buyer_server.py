#from concurrent import futures
#import time
from flask import Flask, request
import grpc
#import mysql.connector
#import sys
import marketplace_pb2_grpc as service
import marketplace_pb2 as message
app = Flask(__name__)

@app.route('/')
def index():
    print("Got the request")
    return "Hello World!"

@app.route('/cart/searchProduct', methods = ['POST'])
def search_products():
    cat_str = request.form.get('id')
    keywords = request.form.get('quantity')
    category = int(cat_str)
    print("category = ",category,"keywords = ", keywords)
    bs = BuyerServer()
    res = bs.search_products(category, keywords)
    print("Response = ", res)
    return res

@app.route('/cart/addItem', methods = ['POST'])
def add_to_cart():
    id_str = request.form.get('id')
    quantity_str = request.form.get('quantity')
    id = int(id_str)
    quantity = int(quantity_str)
    print("id = ",id,"quantity = ", quantity)
    bs = BuyerServer()
    res = bs.add_to_cart(id, quantity)
    print("Response = ", res)
    return res

@app.route('/cart/removeItem', methods = ['POST'])
def remove_from_cart():
    id_str = request.form.get('id')
    quantity_str = request.form.get('quantity')
    id = int(id_str)
    quantity = int(quantity_str)
    print("id = ", id, "quantity = ", quantity)
    bs = BuyerServer()
    res = bs.remove_from_cart(id, quantity)
    print("Response  = ", res)
    return res

@app.route('/cart/clear', methods = ['GET'])
def clear_cart():
    bs = BuyerServer()
    res = bs.clear_cart()
    print("Response = ", res)
    return res

@app.route('/cart/display', methods = ['GET'])
def display_cart():
    bs = BuyerServer()
    res = bs.display_cart()
    print("Response = ", res)
    return res

@app.route('/user/createUser', methods = ['POST'])
def create_user():
    username = request.form.get('username')
    password = request.form.get('password')
    bs = BuyerServer()
    res = bs.create_user(username, password)
    print("Response = ", res)
    return res

@app.route('/user/login', methods = ['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    bs = BuyerServer()
    res = bs.login(username, password)
    print("Response = ", res)
    return res

@app.route('/user/logout', methods = ['POST'])
def logout():
    cookie = request.form.get('cookie')
    bs = BuyerServer()
    res = bs.logout(cookie)
    print("Response = ", res)
    return res

@app.route('/purchase', methods = ['POST'])
def purchase():
    name = request.form.get('name')
    number = request.form.get('number')
    expiration = request.form.get('expiration')
    bs = BuyerServer()
    res = bs.purchase(name, number, expiration)
    print("Response = ", res)
    return res

@app.route('/feedback', methods = ['POST'])
def feedback():
    item_id_str = request.form.get('item_id')
    item_id = int(item_id_str)
    item_review = request.form.get('item_review')
    cookie = request.form.get('cookie')
    bs = BuyerServer()
    res = bs.feedback(item_id, item_review, cookie)
    print("Response = ", res)
    return res

@app.route('/rating', methods = ['POST'])
def rating():
    seller_id_str = request.form.get('seller_id')
    seller_id = int(seller_id_str)
    cookie = request.form.get('cookie')
    bs = BuyerServer()
    res = bs.rating(seller_id, cookie)
    print("Response = ", res)
    return res

@app.route('/history', methods = ['POST'])
def history():
    cookie = request.form.get('cookie')
    bs = BuyerServer()
    res = bs.rating(cookie)
    print("Response = ", res)
    return res



class BuyerServer():
    def __init__(self):
        self.host = 'localhost'
        self.port = 8090

        self.channel = grpc.insecure_channel(
                        '{}:{}'.format(self.host, self.port))

        self.stub = service.marketplaceStub(self.channel)

    def search_products(self, category, keywords):
        req = message.SearchRequest(category=category, keywords=keywords)
        return self.stub.search(req)

    def add_to_cart(self, id, quantity):
        req = message.Item(id=id, quantity=quantity)
        return self.stub.add(req)

    def remove_from_cart(self, id, quantity):
        req = message.Item(id=id, quantity=quantity)
        return self.stub.remove(req)

    def clear_cart(self):
        req = message.void()
        return self.stub.clear(req)

    def display_cart(self):
        req = message.void()
        return self.stub.display(req)
    
    def create_user(self, username, password):
        req = message.UserRequest(username=username, password=password)
        return self.stub.createUser(req)
    
    def login(self, username, password):
        req = message.LoginRequest(username=username, password=password)
        return self.stub.login(req)

    def logout(self, cookie):
        req = message.LogoutRequest(cookie=cookie)
        return self.stub.logout(req)
    
    def purchase(self, name, number, expiration):
        req = message.PurchaseRequest(name=name, number=number, expiration=expiration)
        return self.stub.purchase(req)
    
    def feedback(self, item_id, item_review, cookie):
        req = message.FeedbackRequest(item_id=item_id, item_review=item_review, cookie=cookie)
        return self.stub.feedback(req)

    def rating(self, seller_id, cookie):
        req = message.RatingRequest(seller_id=seller_id, cookie=cookie)
        return self.stub.rating(req)

    def history(self, cookie):
        req = message.HistoryRequest(cookie=cookie)
        return self.stub.history(req)


if __name__ == "__main__":
    app.run(debug=True)
    print('Server running with flask')
