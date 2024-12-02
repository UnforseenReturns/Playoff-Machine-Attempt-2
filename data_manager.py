import json

def load_game_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_game_data(file_path, game_data):
    with open(file_path, 'w') as file:
        json.dump(game_data, file, indent=4)