#!venv/bin/python3.11

import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)

print('coucou')
uri = 'mongodb://root:dicesil2@mongo:27017/METEO_CENTER'
database = db.Database(uri)
data = {}
message = ""

database.adding_sensor_station("ff:ff", "test", "Nancy")

# Route pour recevoir les données du pico
@app.route("/pico-data", methods=["POST"])
def receive_data():
    content = request.json
    global data
    data = content
    database.adding_statement(
        data["mac"], data["temp"], data["humid"], data["pression"]
    )
    return jsonify({"status": "success"}), 200


# Route pour retourner les données du Pico au front
@app.route("/pico-data", methods=["GET"])
def return_data():
    global data
    return jsonify({"status": "success", "message": data}), 200


# Route pour que le Pico obtienne le message
@app.route("/message", methods=["GET"])
def get_message():
    global message
    message = "NONE" if message == "" else message
    return jsonify({"message": message})


@app.route("/message", methods=["POST"])
def set_message():
    data = request.json
    msg = data["message"]
    global message
    if isinstance(msg, str):
        message = msg
        return jsonify({"status": "success"}), 200
    else:
        print("error loading message : " + str(msg))
        return jsonify({"status": "error", "message": "cannot load given message"}), 400


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", data=data)


# Route pour ajouter une nouvelle station
@app.route("/add-station", methods=["POST"])
def add_station():
    global database
    data = request.json
    response = database.adding_sensor_station(data["mac"], data['name'], data["city"])
    if response:
        return jsonify({"status": "success", "message": str(response)}), 200
    else:
        return jsonify({"status": "error"}), 400


# test
@app.route("/print-data", methods=["GET"])
def print_data():
    # data = database.retrieve_statements()
    data = database.print_collections()
    print(data)
    return jsonify({"status": "success", "message": str(data)}), 200


@app.route("/drop", methods=["GET"])
def drop_table():
    global database
    database.drop()
    return jsonify({'status': 'success'}), 200

@app.route('/print-db', methods=["GET"])
def print_db():
    database.print_db()
    return jsonify({'status': 'success'}), 200

@app.route('/print-readme', methods=['GET'])
def readme():
    database.print_readme_to_recover()
    return jsonify({'status': 'success'}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
