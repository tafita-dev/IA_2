from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def connect_to_database():
    try:
        # Connexion à MongoDB
        client = MongoClient("mongodb+srv://tafita:tafita8k@database.ctnbaew.mongodb.net/data?retryWrites=true&w=majority&appName=mpiompy")
        
        # Tentative de connexion à la base de données pour vérifier
        client.admin.command('ping')  # Commande ping pour tester la connexion

        print("Connexion à MongoDB réussie!")
        return client
    except ConnectionFailure as e:
        print(f"Erreur de connexion à MongoDB: {e}")
        return None
