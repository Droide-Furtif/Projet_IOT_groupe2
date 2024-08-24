from pymongo import MongoClient, errors
from datetime import datetime
import os

class Database:
	def __init__(self,uri,db_name):
		self.uri = uri
		self.client = MongoClient(self.uri)
		self.db_name = db_name
		self.db = self.client[self.db_name]
		print(f"Connected to database{self.db}")
	
	#Sensor_Station
	
	def adding_sensor_station(self, mac_id, name, city):
		'''Adding a sensor station with the mac Id, the name and the city of the sensor.'''
		try:
			creation_date = datetime.now().strftime("%d-%m-%Y")
			sensor_station_data = {
				"Mac_Id": mac_id,
				"Name": name,
				"City": city,
				"Creation_Date": creation_date
			}
			sensor_station = self.db.Sensor_Station.insert_one(sensor_station_data).inserted_id
			return 0
		except errors.PyMongoError as e:
			print(f"Erreur lors de l'insertion des données : {e}")
			return 1
	
	def retrieve_all_sensor_station(self):
		try:
			results = self.db.Sensor_Station.find()
			return list(results)  # Convertit le curseur en liste de dictionnaires
		except errors.PyMongoError as e:
			print(f"Erreur lors de la récupération des données : {e}")
			return 1
	
	def sensor_station_exist(self,mac_id):
		try:
			query = {"Mac_Id": mac_id}
			sensor_station = self.db.Sensor_Station.find_one(query)
			return True
		except errors.PyMongoError as e:
			print("error finding Mac Id")
			return False
			
	#Statements
			
	def adding_statement(self, mac_id, temperature, humidity, pressure):
		'''Adding a statement linked to a sensor station. Needing sensor_station_id, temperature, humidity & pressure.'''
		# Check if the sensor station exist with the secret key
		if sensor_station_exist(mac_id):
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
				self.db.Statement.insert_one(statement_data)
				print(f"Données transmises avec succès.\r ID : {result.inserted_id}")
				return 0
			except errors.PyMongoError as e:
				print(f"Erreur lors de l'insertion des données : {e}")
				return 1
		else:
			print("Le capteur n'a pas été trouvé dans la base.")
			return 1

	def retrieve_all_statements(self):
		try:
			results = self.db.Statement.find()
			return list(results)  # Convertit le curseur en liste de dictionnaires
		except errors.PyMongoError as e:
			print(f"Erreur lors de la récupération des données : {e}")
			return 1
	
	def list_all_collections(self):
		return list(self.db.list_collections_names())
