import tkinter as tk
from tkinter import ttk
import json

# Load JSON data
with open('teams.json') as f:
    data = json.load(f)
teams = data['teams']
games = data['games']

# Create the main window
root = tk.Tk()
root.title("Playoff Machine")

# Define the grid layout
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Game Viewer
game_viewer_frame = ttk.Frame(root, padding="10")
game_viewer_frame.grid(row=0, column=0, sticky="nsew")
ttk.Label(game_viewer_frame, text="Game Viewer").pack()

# Listbox to display games
game_listbox = tk.Listbox(game_viewer_frame)
for game in games:
    game_listbox.insert(tk.END, f"Week {game['week']}: {game['team1']} vs {game['team2']} - Winner: {game['winner']}")
game_listbox.pack(fill=tk.BOTH, expand=True)

# Result Updater
result_updater_frame = ttk.Frame(root, padding="10")
result_updater_frame.grid(row=0, column=1, sticky="nsew")
ttk.Label(result_updater_frame, text="Result Updater").pack()

# Standings Display
standings_display_frame = ttk.Frame(root, padding="10")
standings_display_frame.grid(row=1, column=0, sticky="nsew")
ttk.Label(standings_display_frame, text="Standings Display").pack()

# Playoff Predictor
playoff_predictor_frame = ttk.Frame(root, padding="10")
playoff_predictor_frame.grid(row=1, column=1, sticky="nsew")
ttk.Label(playoff_predictor_frame, text="Playoff Predictor").pack()

# Run the application
root.mainloop()