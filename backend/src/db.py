from pymongo import MongoClient, errors
from datetime import datetime
import uuid
import os

class Database:
	def __init__(self,uri):
		self.uri = os.environ['MONGO_URI']
		self.client = None
		self.db = None
		self.sensor_station = None
		self.statement = None
		self.init_db()

	def init_db(self):
		try:
			print(000)
			print(self.uri)
			self.client = MongoClient(self.uri)
			print(self.client)
			self.db = self.client.METEO_CENTER
			print(self.db)
			# self.db = self.client['METEO_CENTER']
			self.sensor_station = self.db['Sensor_Station']
			self.statement = self.db['Statement']
			print("Connexion à la base de données réussie")
		except errors.ServerSelectionTimeoutError as err:
			print(f"Erreur de connexion à la base de données : {err}")

	def retrieve_statements(self):
		try:
			results = self.statement.find({})
			return list(results)  # Convertit le curseur en liste de dictionnaires
		except errors.PyMongoError as e:
			print(f"Erreur lors de la récupération des données : {e}")
			return []

	def retrieve_sensor_station(self):
		try:
			results = self.sensor_station.find({})
			return list(results)  # Convertit le curseur en liste de dictionnaires
		except errors.PyMongoError as e:
			print(f"Erreur lors de la récupération des données : {e}")
			return []

	def adding_sensor_station(self, mac_id, name, city):
		print('adding_sensor_station')

		'''Adding a sensor station with the mac Id, the name and the city of the sensor.'''
		if self.sensor_station is not None:
			print('is not NONE')
			print()
			secret_key = uuid.uuid4()
			creation_date = datetime.now().strftime("%d-%m-%Y")
			sensor_station_data = {
				"Mac_Id": mac_id,
				"Secret_Key": "1234",
				"Name": name,
				"City": city,
				"Creation_Date": creation_date
			}
			try:
				print('ici')
				print(sensor_station_data)
				result = self.sensor_station.insert_one(sensor_station_data)
				print(f"Entrée ajoutée avec l'ID : {result.inserted_id}")
				return result.inserted_id
			except errors.PyMongoError as e:
				print(f"Erreur lors de l'insertion des données : {e}")
				return 0
		else:
			print("La collection 'Sensor_Station' n'est pas disponible")
			return 0

	def adding_statement(self, secret_key, temperature, humidity, pressure):
		'''Adding a statement linked to a sensor station. Needing secret key, the temperatyre, the humidity and the pressure.'''
		if self.sensor_station is not None :
			# Check if the sensor station exist with the secret key
			sensor_station = None
			try:
				query = {"Secret_Key": "1234"}
				sensor_station = self.sensor_station.find_one(query)
			except errors.PyMongoError as e:
				print("error finding secret key")
			if sensor_station is not None:
				# Set the sensor station id to link the statement with the sensor.
				id_sensor_station = sensor_station.get("_id")
				if self.statement is not None:
					date = datetime.now().strftime("%d-%m-%Y")
					time = datetime.now().strftime("%H:%M:%S")
					statement_data = {
						"Id_Sensor_Station_F": id_sensor_station,
						"Temperature": temperature,
						"Humidity": humidity,
						"Pressure": pressure,
						"Date": date,
						"Time": time
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
		else:
			print("La collection 'Sensor_Station' n'est pas disponible")
			return 0