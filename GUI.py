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

# Notebook (tabs)
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, columnspan=2, rowspan=2, sticky="nsew")

# Create a dictionary to hold the frames for each week
week_frames = {}

# Create tabs for each week
for game in games:
    week = game['week']
    if week not in week_frames:
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text=f"Week {week}")
        week_frames[week] = frame
    listbox = tk.Listbox(week_frames[week])
    listbox.pack(fill=tk.BOTH, expand=True)
    listbox.insert(tk.END, f"{game['team1']} vs {game['team2']} - Winner: {game['winner']}")

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