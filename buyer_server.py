from flask import Flask, request
import requests
import grpc
import marketplace_pb2_grpc as service
import marketplace_pb2 as message
app = Flask(__name__)

@app.route('/')
def index():
    print("Got the request")
    return "Hello World!"

@app.route('/cart/searchProduct', methods = ['POST'])
def search_products():
    category = int(request.form.get('category'))
    keywords = request.form.get('keywords')
    print("category = ",category,"keywords = ", keywords)
    bs = BuyerServer()
    res = bs.search_products(category, keywords)
    print("Response = ", res)
    return str(res)

@app.route('/cart/addItem', methods = ['POST'])
def add_to_cart():
    item_id_str = request.form.get('item_id')
    u_id_str = request.form.get('u_id')
    quantity_str = request.form.get('quantity')
    item_id = int(item_id_str)
    u_id = int(u_id_str)
    quantity = int(quantity_str)
    print("item_id = ", item_id,"u_id = ", u_id, "quantity = ", quantity)
    bs = BuyerServer()
    res = bs.add_to_cart(item_id, u_id, quantity)
    print("Response = ", res)
    return str(res)

@app.route('/cart/removeItem', methods = ['POST'])
def remove_from_cart():
    item_id_str = request.form.get('item_id')
    u_id_str = request.form.get('u_id')
    quantity_str = request.form.get('quantity')
    item_id = int(item_id_str)
    u_id = int(u_id_str)
    quantity = int(quantity_str)
    print("item_id = ", item_id, "u_id = ", u_id, "quantity = ", quantity)
    bs = BuyerServer()
    res = bs.remove_from_cart(item_id, u_id, quantity)
    print("Response  = ", res)
    return str(res)

@app.route('/cart/clear', methods = ['POST'])
def clear_cart():
    u_id_str = request.form.get('u_id')
    u_id = int(u_id_str)
    bs = BuyerServer()
    res = bs.clear_cart(u_id)
    print("Response = ", res)
    return str(res)

@app.route('/cart/display', methods = ['POST'])
def display_cart():
    u_id_str = request.form.get('u_id')
    u_id = int(u_id_str)
    bs = BuyerServer()
    res = bs.display_cart(u_id)
    print("Response = ", res)
    return str(res)

@app.route('/user/createUser', methods = ['POST'])
def create_user():
    username = request.form.get('username')
    password = request.form.get('password')
    bs = BuyerServer()
    res = bs.create_user(username, password)
    print("Response = ", res)
    return str(res)

@app.route('/user/login', methods = ['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    bs = BuyerServer()
    res = bs.login(username, password)
    print("Response = ", res)
    return str(res)

@app.route('/user/logout', methods = ['POST'])
def logout():
    u_id = int(request.form.get('u_id'))
    bs = BuyerServer()
    res = bs.logout(u_id)
    print("Response = ", res)
    return str(res)

@app.route('/purchase', methods = ['POST'])
def purchase():
    name = request.form.get('name')
    number = request.form.get('number')
    expiration = request.form.get('expiration')
    u_id = int(request.form.get('u_id'))

    # SOAP Communications

    # location of transaction service
    url = "http://10.180.0.8:6000/transaction"

    # XML payload
    # From: https://www.geeksforgeeks.org/making-soap-api-calls-using-python/
    payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n" \
            + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\n" \
            + "<soap:Body>\n"\
            + "<name>" + name + "</name>\n" \
            + "<number>" + number + "</number>\n" \
            + "<expiration>" + expiration + "</expiration>\n" \
            + "</soap:Body>\n</soap:Envelope>"

    # headers
    headers = {
        'Content-Type': 'text/xml; charset=utf-8'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # If unsuccessful, return "NO"
    if(response.text == "No"):
        return "Credit card declined"
    else:
        bs = BuyerServer()
        res = bs.purchase(name, number, expiration, u_id)
        print("Response = ", res)
        return str(res)

@app.route('/feedback', methods = ['POST'])
def feedback():
    item_id_str = request.form.get('item_id')
    item_id = int(item_id_str)
    item_review = request.form.get('item_review')
    u_id = int(request.form.get('u_id'))
    bs = BuyerServer()
    res = bs.feedback(item_id, item_review, u_id)
    print("Response = ", res)
    return str(res)

@app.route('/rating', methods = ['POST'])
def rating():
    s_id = int(request.form.get('s_id'))
    bs = BuyerServer()
    res = bs.rating(s_id)
    print("Response = ", res)
    return str(res)

@app.route('/history', methods = ['POST'])
def history():
    u_id = int(request.form.get('u_id'))
    bs = BuyerServer()
    res = bs.history(u_id)
    print("Response = ", res)
    return str(res)



class BuyerServer():
    def __init__(self):
        self.host = '10.180.0.4'
        self.port = 8090

        self.channel = grpc.insecure_channel(
                        '{}:{}'.format(self.host, self.port))

        self.stub = service.marketplaceStub(self.channel)

    def search_products(self, category, keywords):
        req = message.SearchRequest(category=category, keywords=keywords)
        return self.stub.search(req)

    def add_to_cart(self, item_id, u_id, quantity):
        req = message.ItemRequest(item_id=item_id, u_id=u_id, quantity=quantity)
        return self.stub.add(req)

    def remove_from_cart(self, item_id, u_id, quantity):
        req = message.ItemRequest(item_id=item_id, u_id=u_id, quantity=quantity)
        return self.stub.remove(req)

    def clear_cart(self, u_id):
        req = message.RequestUid(u_id=u_id)
        return self.stub.clear(req)

    def display_cart(self, u_id):
        req = message.RequestUid(u_id=u_id)
        return self.stub.display(req)
    
    def create_user(self, username, password):
        req = message.UserRequest(username=username, password=password)
        return self.stub.createUser(req)
    
    def login(self, username, password):
        req = message.LoginRequest(username=username, password=password)
        return self.stub.login(req)

    def logout(self, u_id):
        req = message.LogoutRequest(u_id=u_id)
        return self.stub.logout(req)
    
    def purchase(self, name, number, expiration, u_id):
        req = message.PurchaseRequest(name=name, number=number, expiration=expiration, u_id=u_id)
        return self.stub.purchase(req)
    
    def feedback(self, item_id, item_review, u_id):
        req = message.FeedbackRequest(item_id=item_id, item_review=item_review, u_id=u_id)
        return self.stub.feedback(req)

    def rating(self, s_id):
        req = message.RatingRequest(s_id=s_id)
        return self.stub.rating(req)

    def history(self, u_id):
        req = message.HistoryRequest(u_id=u_id)
        return self.stub.history(req)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    print('Server running with flask')
