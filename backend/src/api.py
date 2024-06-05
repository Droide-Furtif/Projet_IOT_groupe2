#!venv/bin/python3.11

import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

data = {}

# Route pour recevoir les données du pico
@app.route('/pico-data', methods=['POST'])
def receive_data():
	content = request.json
	print((f"Température: {content['temp']}°C\n"
		f"Pression: {content['pression']}hPa\n"
		f"Humidité: {content['humid']}%\n"))
	global data
	data = content
	return jsonify({'status': 'success'}), 200

# Route pour retourner les données du Pico au front
@app.route('/pico-data', methods=['GET'])
def return_data():
	global data
	return jsonify({'status': 'success', 'message': data}), 200

# Route pour que le Pico obtienne le message
@app.route('/message', methods=['GET'])
def get_data():
	message = "Bonjour internet"
	return jsonify({"message": message})


@app.route('/', methods=['GET'])
def index():
	print("ah")
	return render_template('index.html', data=data)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port="5000", debug=True)
