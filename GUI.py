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

# Function to load and resize team logos
def load_logo(team_name, size):
    logo_path = os.path.join('logos', f"{team_name}.png")
    if os.path.exists(logo_path):
        image = Image.open(logo_path)
        image = image.resize((size, size), Image.LANCZOS)
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

# Function to update the GUI layout based on window size
def update_layout(event):
    width = max(event.width // 12, 1)
    height = max(event.height // 12, 1)
    size = min(width, height)
    for game in games:
        week = game['week']
        frame = week_frames[week]
        team1_logo = load_logo(game['team1'], size)
        team2_logo = load_logo(game['team2'], size)
        winner_logo = load_logo(game['winner'], size)
        
        # Update existing labels with new images
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Label) and hasattr(widget, 'image_path'):
                if widget.image_path == game['team1']:
                    widget.config(image=team1_logo)
                    widget.image = team1_logo
                elif widget.image_path == game['team2']:
                    widget.config(image=team2_logo)
                    widget.image = team2_logo
                elif widget.image_path == game['winner']:
                    widget.config(image=winner_logo)
                    widget.image = winner_logo

for game in games:
    week = game['week']
    if week not in week_frames:
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text=f"Week {week}")
        week_frames[week] = frame

    frame = ttk.Frame(week_frames[week])
    frame.pack(fill=tk.BOTH, expand=True)

    # Determine the row and column based on the game's index
    game_index = games.index(game)
    row = game_index % 8
    col = (game_index // 8) * 6

    # Create initial logos with a default size
    team1_logo = load_logo(game['team1'], 50)
    team2_logo = load_logo(game['team2'], 50)
    winner_logo = load_logo(game['winner'], 50)

    if team1_logo:
        label_team1 = tk.Label(frame, image=team1_logo)
        label_team1.image = team1_logo
        label_team1.image_path = game['team1']  # Store path for resizing
        label_team1.grid(row=row, column=col)

    vs_label = tk.Label(frame, text=" vs ")
    vs_label.grid(row=row, column=col + 1)

    if team2_logo:
        label_team2 = tk.Label(frame, image=team2_logo)
        label_team2.image = team2_logo
        label_team2.image_path = game['team2']  # Store path for resizing
        label_team2.grid(row=row, column=col + 2)

    winner_label = tk.Label(frame, text=" - Winner: ")
    winner_label.grid(row=row, column=col + 3)

    if winner_logo:
        label_winner = tk.Label(frame, image=winner_logo)
        label_winner.image = winner_logo
        label_winner.image_path = game['winner']  # Store path for resizing
        label_winner.grid(row=row, column=col + 4)

# Bind the resize event to the update_layout function
root.bind('<Configure>', update_layout)

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
