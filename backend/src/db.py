from pymongo import MongoClient, errors
from datetime import date
import os

class Database:
	def __init__(self):
		self.client = None
		self.db = None
		self.sensor_station = None
		self.statement = None
		self.init_db()


	def init_db(self):
		try:
			self.client = MongoClient(host='mongodb', port=27017, serverSelectionTimeoutMS=5000)
			self.client.server_info()
			self.db = self.client['METEO_CENTER']
			self.sensor_station = self.db['Sensor_Station']
			self.statement = self.db['Statement']
			print("Connexion à la base de données réussie")
		except errors.ServerSelectionTimeoutError as err:
			print(f"Erreur de connexion à la base de données : {err}")

	def adding_sensor_station(self, mac_id, city):
		if self.sensor_station is not None:
			creation_date = date.today().strftime("%d-%m-%Y")
			sensor_station_data = {
				"mac_id": mac_id,
				"city": city,
				"creation_date": creation_date
			}
			try:
				result = self.sensor_station.insert_one(sensor_station_data)
				print(f"Entrée ajoutée avec l'ID : {result.inserted_id}")
				return result.inserted_id
			except errors.PyMongoError as e:
				print(f"Erreur lors de l'insertion des données : {e}")
				return 0
		else:
			print("La collection 'Sensor_Station' n'est pas disponible")
			return 0

	def adding_statement(self, temperature, humidity, pressure):
		if self.statement is not None:
			date = date.today().strftime("%d-%m-%Y")
			time = date.time()strftime("%H:%M:%S")
			statement_data = {
				"temperature": temperature,
				"humidity": humidity,
				"pressure": pressure,
				"date": date,
				"time"
			}
			try:
				result = self.statement.insert_one(statement_data)
				print(f"Données transmises avec succès.\r ID : {result.inserted_id}")
				return 1
			except errors.PyMongoError as e:
				print(f"Erreur lors de l'insertion des données : {e}")
				return 0
		else:
			print("La collection 'Statement' n'est pas disponible")
			return 0