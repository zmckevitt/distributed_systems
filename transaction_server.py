from flask import Flask, request
import random
import xmltodict
app = Flask(__name__)


@app.route('/transaction', methods = ['POST'])
def transaction():
	xml = request.data.decode('utf-8')
	d = xmltodict.parse(xml)

	name = d['soap:Envelope']['soap:Body']['name']
	number = d['soap:Envelope']['soap:Body']['number']
	expiration = d['soap:Envelope']['soap:Body']['expiration']

	print("Name: ", name)
	print("Number: ", number)
	print("Expiration: ", expiration)

	rng = random.randint(0,100)

	if(rng > 5):
		return "Yes"
	else:
		return "No"

if __name__ == "__main__":
	app.run(host='10.180.0.8', port=6000, debug=True)
	#app.run(host='127.0.0.1', port=6000, debug=True)
	print('Server running with flask')
