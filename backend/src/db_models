from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from collections import OrderedDict

class Db_Model:
    def __init__(self,uri):
        self.uri = os.environ['MONGO_URI']
        self.client = None
		self.db = None
        self.db_name = None
		self.collection = None
        self.collection_name = None
		self.init_db_model()

	def init_db_model(self):
		try:
			self.client = MongoClient(self.uri)
			self.db = self.client[self.db_name]
			self.collection = self.db[self.collection_name]
			print("Connexion à la base de données réussie")
		except errors.ServerSelectionTimeoutError as err:
			print(f"Erreur de connexion à la base de données : {err}")

    def add_collection_model(self, schema):
        try:
            collection = {self.collection_name, schema}
            validator = {'$jsonSchema': {'bsonType': 'object', 'properties': {}}}
            required = []

            for field_key in schema:
            field = schema[field_key]
            properties = {'bsonType': field['type']}
            minimum = field.get('minlength')

            if type(minimum) == int:
                properties['minimum'] = minimum

            if field.get('required') is True: required.append(field_key)
                validator['$jsonSchema']['properties'][field_key] = properties

            if len(required) > 0:
                validator['$jsonSchema']['required'] = required
                query = [('collMod', collection),('validator', validator)]

            try:
                print("Collection ajoutée")
                db.create_collection(collection)
            except CollectionInvalid as e:
                print(f"Collection invalide : \n{e}")

            command_result = db.command(OrderedDict(query))
        except errors.ServerSelectionTimeoutError as err:
			print(f"Problème lors de l'ajout de la collection : \n{err}")

# Exemple of schema to create a colection
# user_schema = {
#     'firstName': {
#         'type': 'string',
#         'minlength': 1,
#         'required': True,
#     },
#     'lastName': {
#         'type': 'string',
#         'minlength': 1,
#         'required': True,
#     },
#     'email': {
#         'type': 'string',
#         "required": False,
#     },
#     'phoneNo': {
#         'type': 'int',
#         'required': True,
#     },
#     'userId': {
#         'type': 'int',
#         'required': True,
#     },
#     'patientId': {
#         'type': 'int',
#         'required': True,
#     },
#     'age': {
#         'type': 'int'
#     },
#     "userStatus": {
#         "type": "int"
#     }
# }