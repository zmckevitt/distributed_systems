from flask import Flask, request
import grpc
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
    keywords = request.form.get('keywords')
    category = int(request.form.get('category'))
    condition = bool(request.form.get('condition'))
    price = float(request.form.get('price'))
    u_id = int(request.form.get('u_id'))

    ss = SellerServer()
    res = ss.sell_product(name, category, keywords, condition, price, u_id)
    print("Response = ", res)
    return str(res)

@app.route('/products/modify', methods = ['POST'])
def modify_product():
    item_id = int(request.form.get('id'))
    price = float(request.form.get('price'))
    u_id = int(request.form.get('u_id'))

    ss = SellerServer()
    res = ss.modify_product(item_id, price, u_id)
    print("Response = ", res)
    return str(res)

@app.route('/products/remove', methods = ['POST'])
def remove_product():
    item_id = int(request.form.get('id'))
    quantity = int(request.form.get('quantity'))
    u_id = int(request.form.get('u_id'))

    ss = SellerServer()
    res = ss.remove_product(item_id, quantity, u_id)
    print("Response = ", res)
    return str(res)

@app.route('/products/list', methods = ['POST'])
def list_products():
    u_id = int(request.form.get('u_id'))

    ss = SellerServer()
    res = ss.list_products(u_id)
    print("Response = ", res)
    return str(res)

@app.route('/user/createUser', methods = ['POST'])
def create_user():
    username = request.form.get('username')
    password = request.form.get('password')
    ss = SellerServer()
    res = ss.create_user(username, password)
    print("Response = ", res)
    return str(res)

@app.route('/user/login', methods = ['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    ss = SellerServer()
    res = ss.login(username, password)
    print("Response = ", res)
    return str(res)

@app.route('/user/logout', methods = ['POST'])
def logout():
    u_id = int(request.form.get('u_id'))
    ss = SellerServer()
    res = ss.logout(u_id)
    print("Response = ", res)
    return str(res)

@app.route('/rating', methods = ['POST'])
def rating():
    u_id = int(request.form.get('s_id'))
    ss = SellerServer()
    res = ss.rating(u_id)
    print("Response = ", res)
    return str(res)

class SellerServer():
    def __init__(self):
        self.host = '10.180.0.7'
        #self.host = '127.0.0.1'
        self.port = 8080

        self.channel = grpc.insecure_channel(
                        '{}:{}'.format(self.host, self.port))

        self.stub = service.marketplaceStub(self.channel)

    def sell_product(self, name, category, keywords, condition, price, u_id):
        req = message.ListItem(name=name, category=category, keywords=keywords, \
                                condition=condition, price=price, u_id=u_id)
        return self.stub.sell(req)

    def modify_product(self, _id, price, u_id):
        req = message.PriceItem(id=_id, price=price, u_id=u_id)
        return self.stub.modify(req)

    def remove_product(self, _id, quantity, u_id):
        req = message.RemoveItem(id=_id, quantity=quantity, u_id=u_id)
        return self.stub.removeListing(req)

    def list_products(self, u_id):
        req = message.ListRequest(u_id=u_id)
        return self.stub.list(req)
    
    def create_user(self, username, password):
        req = message.UserRequest(username=username, password=password)
        return self.stub.createUser(req)
    
    def login(self, username, password):
        req = message.LoginRequest(username=username, password=password)
        return self.stub.login(req)

    def logout(self, u_id):
        req = message.LogoutRequest(u_id=u_id)
        return self.stub.logout(req)

    def rating(self, s_id):
        req = message.RatingRequest(s_id=s_id)
        return self.stub.rating(req)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(host='127.0.0.1', port=5000, debug=True)
    print('Server running with flask')
