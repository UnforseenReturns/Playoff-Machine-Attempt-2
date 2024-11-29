import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json
import os

# Create the main window
root = tk.Tk()
root.title("Playoff Machine")

# Load JSON data
with open('teams.json') as f:
    data = json.load(f)
teams = data['teams']
games = data['games']

# Preload team logos
team_logos = {}
for team in teams:
    logo_path = os.path.join('logos', f"{team['name']}.png")
    if os.path.exists(logo_path):
        image = Image.open(logo_path)
        image = image.resize((50, 50), Image.LANCZOS)
        team_logos[team['name']] = ImageTk.PhotoImage(image)
    else:
        print(f"Logo not found for {team['name']}")

# Compute win/loss records
records = {team['name']: {'wins': 0, 'losses': 0, 'head_to_head': {}} for team in teams}
for game in games:
    if game['winner']:
        if game['winner'] == game['team1']:
            records[game['team1']]['wins'] += 1
            records[game['team2']]['losses'] += 1
        else:
            records[game['team1']]['losses'] += 1
            records[game['team2']]['wins'] += 1

    # Update head-to-head
    if game['winner']:
        if game['team1'] in records[game['team2']]['head_to_head']:
            records[game['team2']]['head_to_head'][game['team1']] += 1
        else:
            records[game['team2']]['head_to_head'][game['team1']] = 1

        if game['team2'] in records[game['team1']]['head_to_head']:
            records[game['team1']]['head_to_head'][game['team2']] += 1
        else:
            records[game['team1']]['head_to_head'][game['team2']] = 1

# Define the grid layout
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

# Notebook (tabs)
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, columnspan=2, rowspan=3, sticky="nsew")

# Create a dictionary to hold the frames for each week
week_frames = {}
weeks = {}
for game in games:
    week = game['week']
    if week not in weeks:
        weeks[week] = 0
    weeks[week] += 1

# Create tabs for each week
for game in games:
    week = game['week']
    if week not in week_frames:
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text=f"Week {week}")
        week_frames[week] = frame

        # Display the number of games for the week
        week_label = ttk.Label(frame, text=f"Number of games in Week {week}: {weeks[week]}")
        week_label.pack(anchor='w')

    team1_logo = team_logos.get(game['team1'])
    team2_logo = team_logos.get(game['team2'])
    winner_logo = team_logos.get(game['winner'])

    game_frame = ttk.Frame(week_frames[week])
    game_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    if team1_logo:
        label_team1 = tk.Label(game_frame, image=team1_logo)
        label_team1.image = team1_logo
        label_team1.pack(side=tk.LEFT)

    vs_label = tk.Label(game_frame, text=" vs ")
    vs_label.pack(side=tk.LEFT)

    if team2_logo:
        label_team2 = tk.Label(game_frame, image=team2_logo)
        label_team2.image = team2_logo
        label_team2.pack(side=tk.LEFT)

    winner_label = tk.Label(game_frame, text=" - Winner: ")
    winner_label.pack(side=tk.LEFT)

    if winner_logo:
        label_winner = tk.Label(game_frame, image=winner_logo)
        label_winner.image = winner_logo
        label_winner.pack(side=tk.LEFT)

# Standings Display
standings_display_frame = ttk.Frame(root, padding="10")
standings_display_frame.grid(row=1, column=1, sticky="nsew")
ttk.Label(standings_display_frame, text="Standings Display").pack()

# Function to update standings
def update_standings():
    for widget in standings_display_frame.winfo_children():
        widget.destroy()
    ttk.Label(standings_display_frame, text="Standings Display").pack()

    conferences = {"AFC": {}, "NFC": {}}
    for team in teams:
        conference = team["conference"]
        division = team["division"]
        if division not in conferences[conference]:
            conferences[conference][division] = []
        conferences[conference][division].append(team["name"])

    # Create a frame for each conference
    afc_frame = ttk.Frame(standings_display_frame)
    afc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    nfc_frame = ttk.Frame(standings_display_frame)
    nfc_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    for conference, divisions in conferences.items():
        conference_frame = afc_frame if conference == "AFC" else nfc_frame
        conference_label = ttk.Label(conference_frame, text=conference, font=("Helvetica", 16))
        conference_label.pack(anchor='w')
        for division, division_teams in divisions.items():
            division_label = ttk.Label(conference_frame, text=division, font=("Helvetica", 14))
            division_label.pack(anchor='w', padx=20)

            # Sort teams by wins in descending order
            sorted_teams = sorted(division_teams, key=lambda t: records[t]['wins'], reverse=True)
            for team in sorted_teams:
                record = records[team]
                team_label = ttk.Label(conference_frame, text=f"{team}: {record['wins']}-{record['losses']}")
                team_label.pack(anchor='w', padx=40)

update_standings()

# Playoff Predictor
playoff_predictor_frame = ttk.Frame(root, padding="10")
playoff_predictor_frame.grid(row=0, column=1, sticky="nsew")
ttk.Label(playoff_predictor_frame, text="Playoff Predictor").pack()

def apply_tiebreakers(teams):
    # Sort by head-to-head
    return sorted(teams, key=lambda t: records[t]['head_to_head'], reverse=True)

def update_playoff_predictor():
    for widget in playoff_predictor_frame.winfo_children():
        widget.destroy()
    ttk.Label(playoff_predictor_frame, text="Playoff Predictor").pack()

    conferences = {"AFC": [], "NFC": []}
    for team in teams:
        conference = team["conference"]
        conferences[conference].append(team["name"])

    afc_frame = ttk.Frame(playoff_predictor_frame)
    afc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    nfc_frame = ttk.Frame(playoff_predictor_frame)
    nfc_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    for conference, conference_teams in conferences.items():
        # Sort teams by wins in descending order
        sorted_teams = sorted(conference_teams, key=lambda t: records[t]['wins'], reverse=True)
        # Apply tiebreakers
        sorted_teams = apply_tiebreakers(sorted_teams)
        top_teams = sorted_teams[:7]
        conference_frame = afc_frame if conference == "AFC" else nfc_frame
        conference_label = ttk.Label(conference_frame, text=f"{conference} Playoff Teams", font=("Helvetica", 16))
        conference_label.pack(anchor='w')
        for seed, team in enumerate(top_teams, 1):
            record = records[team]
            team_frame = ttk.Frame(conference_frame)
            team_frame.pack(anchor='w', padx=40)
            team_logo = team_logos.get(team)
            if team_logo:
                logo_label = tk.Label(team_frame, image=team_logo)
                logo_label.image = team_logo
                logo_label.pack(side=tk.LEFT)
            team_label = ttk.Label(team_frame, text=f"Seed {seed}: {team} ({record['wins']}-{record['losses']})")
            team_label.pack(side=tk.LEFT)

update_playoff_predictor()

# Run the application
root.mainloop()
