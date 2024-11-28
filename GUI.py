import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # You need to install Pillow for image handling
import json
import os

# Load JSON data
with open('teams.json') as f:
    data = json.load(f)
teams = data['teams']
games = data['games']

# Function to load team logos
def load_logo(team_name):
    logo_path = os.path.join('logos', f"{team_name}.png")
    if os.path.exists(logo_path):
        print(f"Loading logo for {team_name} from {logo_path}")
        image = Image.open(logo_path)
        image = image.resize((50, 50), Image.LANCZOS)  # Updated to Image.LANCZOS
        return ImageTk.PhotoImage(image)
    print(f"Logo not found for {team_name}")
    return None

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
team_logos = {}

# Create tabs for each week
for game in games:
    week = game['week']
    if week not in week_frames:
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text=f"Week {week}")
        week_frames[week] = frame

    team1_logo = load_logo(game['team1'])
    team2_logo = load_logo(game['team2'])
    winner_logo = load_logo(game['winner'])

    frame = ttk.Frame(week_frames[week])
    frame.pack(fill=tk.BOTH, expand=True)

    if team1_logo:
        label_team1 = tk.Label(frame, image=team1_logo)
        label_team1.image = team1_logo  # Keep a reference to avoid garbage collection
        label_team1.pack(side=tk.LEFT)

    vs_label = tk.Label(frame, text=" vs ")
    vs_label.pack(side=tk.LEFT)

    if team2_logo:
        label_team2 = tk.Label(frame, image=team2_logo)
        label_team2.image = team2_logo  # Keep a reference to avoid garbage collection
        label_team2.pack(side=tk.LEFT)

    winner_label = tk.Label(frame, text=" - Winner: ")
    winner_label.pack(side=tk.LEFT)

    if winner_logo:
        label_winner = tk.Label(frame, image=winner_logo)
        label_winner.image = winner_logo  # Keep a reference to avoid garbage collection
        label_winner.pack(side=tk.LEFT)
        
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
