import json
import hashlib
import os

DATA_FILE = "players.json"
CACHE_FILE = "cache.json"

def load_players():
    """Charge les données des joueurs depuis le fichier JSON."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

def save_players(players):
    """Sauvegarde les données des joueurs dans le fichier JSON."""
    with open(DATA_FILE, "w") as file:
        json.dump(players, file, indent=4)

def hash_password(password):
    """Crée un hash sécurisé pour le mot de passe."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_cache():
    """Charge les données du cache."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            return json.load(file)
    return None

def save_cache(username, player_data):
    """Sauvegarde les données dans le cache."""
    with open(CACHE_FILE, "w") as file:
        json.dump({"username": username, "player_data": player_data}, file, indent=4)

def clear_cache():
    """Supprime le contenu du cache sans supprimer le fichier."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "w") as file:
            json.dump({}, file, indent=4)
    

def authentication(username, password):
    players = load_players()
    hashed_password = hash_password(password)
    if username in players and players[username]["password"] == hashed_password:
        save_cache(username, players[username])
        return players[username]
    return None

def register(username, password):
    """Crée un nouveau compte utilisateur."""
    players = load_players()

    if username == "":
        username = input("Créer un nom d'utilisateur : ")
    if username in players:
        print("Ce nom d'utilisateur existe déjà.")
        return None, None

    if password == "":
        password = input("Créer un mot de passe : ")
    hashed_password = hash_password(password)

    players[username] = {
        "password": hashed_password,
        "health": 1,
        "health_lvl": 1,
        "strength": 0.5,
        "strength_lvl": 1,
        "shooting": 0.75,
        "shooting_lvl": 1,
        "coins": 0,
        "total_jump": 0,
        "total_kill": 0,
        "total_death": 0
    }

    save_players(players)
    save_cache(username, players[username])  # Save to cache after registration
    print("Compte créé avec succès !")
    return username, players[username]