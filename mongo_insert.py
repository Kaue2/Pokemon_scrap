from pymongo import MongoClient
import os
import json

connection_string = f"mongodb+srv://{os.getenv("MONGO_USER")}:{os.getenv("MONGO_PASSWORD")}@pokemondb.e1aohue.mongodb.net/?retryWrites=true&w=majority&appName=PokemonDB"

client = MongoClient(connection_string)

db = client["PokemonDB"]

collection = db["Pokemon_collection"]

data = None

with open("pokemon_tratado.json", "r") as f:
    data = json.load(f)
    
if data is None:
    print("Erro ao ler arquivo")

collection.insert_many(data)
