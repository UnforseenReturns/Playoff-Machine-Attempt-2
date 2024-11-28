import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
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
        image = Image.open(logo_path)
        image = image.resize((50, 50), Image.LANCZOS)
        return ImageTk.PhotoImage(image)
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

for game in games:
    week = game['week']
    if week not in week_frames:
        container = ttk.Frame(notebook, padding="10")
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        notebook.add(container, text=f"Week {week}")
        week_frames[week] = scrollable_frame

        container.pack(fill=tk.BOTH, expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    frame = week_frames[week]

    # Determine the row and column based on the game's index
    game_index = games.index(game)
    row = game_index % 8
    col = (game_index // 8) * 6

    team1_logo = load_logo(game['team1'])
    team2_logo = load_logo(game['team2'])
    winner_logo = load_logo(game['winner'])

    if team1_logo:
        label_team1 = tk.Label(frame, image=team1_logo)
        label_team1.image = team1_logo
        label_team1.image_path = game['team1']
        label_team1.grid(row=row, column=col)

    vs_label = tk.Label(frame, text=" vs ")
    vs_label.grid(row=row, column=col + 1)

    if team2_logo:
        label_team2 = tk.Label(frame, image=team2_logo)
        label_team2.image = team2_logo
        label_team2.image_path = game['team2']
        label_team2.grid(row=row, column=col + 2)

    winner_label = tk.Label(frame, text=" - Winner: ")
    winner_label.grid(row=row, column=col + 3)

    if winner_logo:
        label_winner = tk.Label(frame, image=winner_logo)
        label_winner.image = winner_logo
        label_winner.image_path = game['winner']
        label_winner.grid(row=row, column=col + 4)

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
