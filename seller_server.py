# import sys
# import socket
# import mysql.connector
# from _thread import *
# import threading

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

@app.route('/products/sell', methods = ['POST'])
def sell_product():
    name = request.form.get('name')
    keywords = request.form.get('quantity')
    category = int(request.form.get('category'))
    condition = bool(request.form.get('condition'))
    price = float(request.form.get('price'))
    cookie = int(request.form.get('cookie'))

    ss = SellerServer()
    res = ss.sell_product(name, category, keywords, condition, price, cookie)
    print("Response = ", res)
    return res

@app.route('/products/modify', methods = ['POST'])
def modify_product():
    item_id = int(request.form.get('id'))
    price = float(request.form.get('price'))
    cookie = int(request.form.get('cookie'))

    ss = SellerServer()
    res = ss.modify_product(item_id, price, cookie)
    print("Response = ", res)
    return res

@app.route('/products/remove', methods = ['POST'])
def remove_product():
    item_id = int(request.form.get('id'))
    quantity = int(request.form.get('quantity'))
    cookie = int(request.form.get('cookie'))

    ss = SellerServer()
    res = ss.remove_product(item_id, quantity, cookie)
    print("Response = ", res)
    return res

@app.route('/products/list', methods = ['POST'])
def list_products():
    cookie = int(request.form.get('cookie'))

    ss = SellerServer()
    res = ss.search_products(cookie)
    print("Response = ", res)
    return res

@app.route('/user/createUser', methods = ['POST'])
def create_user():
    username = request.form.get('username')
    password = request.form.get('password')
    ss = SellerServer()
    res = ss.create_user(username, password)
    print("Response = ", res)
    return res

@app.route('/user/login', methods = ['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    ss = SellerServer()
    res = ss.login(username, password)
    print("Response = ", res)
    return res

@app.route('/user/logout', methods = ['POST'])
def logout():
    cookie = request.form.get('cookie')
    ss = SellerServer()
    res = ss.logout(cookie)
    print("Response = ", res)
    return res

@app.route('/rating', methods = ['POST'])
def rating():
    seller_id_str = request.form.get('seller_id')
    seller_id = int(seller_id_str)
    cookie = request.form.get('cookie')
    ss = SellerServer()
    res = ss.rating(seller_id, cookie)
    print("Response = ", res)
    return res

class SellerServer():
    def __init__(self):
        self.host = 'localhost'
        self.port = 8080

        self.channel = grpc.insecure_channel(
                        '{}:{}'.format(self.host, self.port))

        self.stub = service.marketplaceStub(self.channel)

    def sell_product(self, name, category, keywords, condition, price, cookie):
        req = message.ListItem(name=name, category=category, keywords=keywords, \
                                condition=condition, price=price, cookie=cookie)
        return self.stub.sell(req)

    def modify_product(self, _id, price, cookie):
        req = message.PriceItem(id=_id, price=price, cookie=cookie)
        return self.stub.modify(req)

    def remove_product(self, _id, quantity):
        req = message.RemoveItem(id=_id, quantity=quantity)
        return self.stub.removeListing(req)

    def list_products(self, cookie):
        req = message.ListRequest(cookie=cookie)
        return self.stub.list(req)
    
    def create_user(self, username, password):
        req = message.UserRequest(username=username, password=password)
        return self.stub.createUser(req)
    
    def login(self, username, password):
        req = message.LoginRequest(username=username, password=password)
        return self.stub.login(req)

    def logout(self, cookie):
        req = message.LogoutRequest(cookie=cookie)
        return self.stub.logout(req)

    def rating(self, seller_id, cookie):
        req = message.RatingRequest(seller_id=seller_id, cookie=cookie)
        return self.stub.rating(req)


if __name__ == "__main__":
    app.run(debug=True)
    print('Server running with flask')
