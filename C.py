import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from data_manager import load_game_data, save_game_data
import sys
import subprocess

# Create the main window
root = tk.Tk()
root.title("Playoff Machine")

# Load JSON data
team_data = load_game_data('teams.json')
teams = team_data['teams']

game_data = load_game_data('games.json')
games = game_data['games']

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

# Initialize records with nested dictionaries for head-to-head outcomes
records = {team['name']: {'wins': 0, 'losses': 0, 'head_to_head': {}, 'outcomes': {}, 'division_wins': 0} for team in teams}

for game in games:
    if game['winner']:
        if game['winner'] == game['team1']:
            records[game['team1']]['wins'] += 1
            records[game['team2']]['losses'] += 1
        else:
            records[game['team1']]['losses'] += 1
            records[game['team2']]['wins'] += 1

        # Update head-to-head
        if game['team1'] in records[game['team2']]['head_to_head']:
            records[game['team2']]['head_to_head'][game['team1']] += 1
        else:
            records[game['team2']]['head_to_head'][game['team1']] = 1

        if game['team2'] in records[game['team1']]['head_to_head']:
            records[game['team1']]['head_to_head'][game['team2']] += 1
        else:
            records[game['team1']]['head_to_head'][game['team2']] = 1

        # Record the outcome of the game
        if game['team1'] not in records[game['team2']]['outcomes']:
            records[game['team2']]['outcomes'][game['team1']] = {'wins': 0, 'losses': 0}
        if game['team2'] not in records[game['team1']]['outcomes']:
            records[game['team1']]['outcomes'][game['team2']] = {'wins': 0, 'losses': 0}

        if game['winner'] == game['team1']:
            records[game['team1']]['outcomes'][game['team2']]['wins'] += 1
            records[game['team2']]['outcomes'][game['team1']]['losses'] += 1
        else:
            records[game['team2']]['outcomes'][game['team1']]['wins'] += 1
            records[game['team1']]['outcomes'][game['team2']]['losses'] += 1

        # Update division wins
        if 'division_game' in game and game['division_game']:
            if game['winner'] == game['team1']:
                records[game['team1']]['division_wins'] += 1
            else:
                records[game['team2']]['division_wins'] += 1

# Function to update game winner
def update_winner(game, winner):
    # Remove previous winner's stats
    previous_winner = game.get('winner')
    if previous_winner:
        if previous_winner == game['team1']:
            records[game['team1']]['wins'] -= 1
            records[game['team2']]['losses'] -= 1
        else:
            records[game['team1']]['losses'] -= 1
            records[game['team2']]['wins'] -= 1

        # Update head-to-head
        if game['team1'] in records[game['team2']]['head_to_head']:
            records[game['team2']]['head_to_head'][game['team1']] -= 1
        if game['team2'] in records[game['team1']]['head_to_head']:
            records[game['team1']]['head_to_head'][game['team2']] -= 1

        # Record the outcome of the game
        if previous_winner == game['team1']:
            records[game['team1']]['outcomes'][game['team2']]['wins'] -= 1
            records[game['team2']]['outcomes'][game['team1']]['losses'] -= 1
        else:
            records[game['team2']]['outcomes'][game['team1']]['wins'] -= 1
            records[game['team1']]['outcomes'][game['team2']]['losses'] -= 1

        # Update division wins
        if 'division_game' in game and game['division_game']:
            if previous_winner == game['team1']:
                records[game['team1']]['division_wins'] -= 1
            else:
                records[game['team2']]['division_wins'] -= 1

    # Add new winner's stats
    game['winner'] = winner
    if winner == game['team1']:
        records[game['team1']]['wins'] += 1
        records[game['team2']]['losses'] += 1
    else:
        records[game['team1']]['losses'] += 1
        records[game['team2']]['wins'] += 1

    # Update head-to-head
    if game['team1'] in records[game['team2']]['head_to_head']:
        records[game['team2']]['head_to_head'][game['team1']] += 1
    else:
        records[game['team2']]['head_to_head'][game['team1']] = 1

    if game['team2'] in records[game['team1']]['head_to_head']:
        records[game['team1']]['head_to_head'][game['team2']] += 1
    else:
        records[game['team1']]['head_to_head'][game['team2']] = 1

    # Record the outcome of the game
    if game['team1'] not in records[game['team2']]['outcomes']:
        records[game['team2']]['outcomes'][game['team1']] = {'wins': 0, 'losses': 0}
    if game['team2'] not in records[game['team1']]['outcomes']:
        records[game['team1']]['outcomes'][game['team2']] = {'wins': 0, 'losses': 0}

    if winner == game['team1']:
        records[game['team1']]['outcomes'][game['team2']]['wins'] += 1
        records[game['team2']]['outcomes'][game['team1']]['losses'] += 1
    else:
        records[game['team2']]['outcomes'][game['team1']]['wins'] += 1
        records[game['team1']]['outcomes'][game['team2']]['losses'] += 1

    # Update division wins
    if 'division_game' in game and game['division_game']:
        if winner == game['team1']:
            records[game['team1']]['division_wins'] += 1
        else:
            records[game['team2']]['division_wins'] += 1

    # Save the updated game data
    save_game_data('games.json', {'teams': teams, 'games': games})

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

    if game['winner']:
        winner_label = tk.Label(game_frame, text=f" - Winner: {game['winner']}")
        winner_label.pack(side=tk.LEFT)
    else:
        # Add a drop-down menu for assigning winner
        winner_var = tk.StringVar()
        winner_menu = ttk.Combobox(game_frame, textvariable=winner_var)
        winner_menu['values'] = (game['team1'], game['team2'])
        winner_menu.set('Select Winner')
        winner_menu.pack(side=tk.LEFT)

        def set_winner(event, game=game, winner_var=winner_var):
            selected_winner = winner_var.get()
            if selected_winner:
                update_winner(game, selected_winner)
                update_standings()
                update_playoff_predictor()

        winner_menu.bind("<<ComboboxSelected>>", set_winner)

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
    def division_record(team):
        return records[team]['division_wins']

    def head_to_head_record(team1, team2):
        return records[team1]['outcomes'].get(team2, {'wins': 0, 'losses': 0})['wins']

    def sort_teams(tiebreaker_teams):
        # Sort by division records first
        sorted_teams = sorted(tiebreaker_teams, key=lambda t: (records[t]['wins'], division_record(t)), reverse=True)
        
        # Apply head-to-head tiebreaker
        for i in range(len(sorted_teams) - 1):
            for j in range(i + 1, len(sorted_teams)):
                if head_to_head_record(sorted_teams[j], sorted_teams[i]) > 0:
                    sorted_teams[i], sorted_teams[j] = sorted_teams[j], sorted_teams[i]
        
        return sorted_teams

    return sort_teams(teams)

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
        # Sort teams by wins in descending order within each division
        divisions = {}
        for team in conference_teams:
            division = next(t['division'] for t in teams if t['name'] == team)
            if division not in divisions:
                divisions[division] = []
            divisions[division].append(team)

        top_division_teams = []
        for division, division_teams in divisions.items():
            sorted_division_teams = sorted(division_teams, key=lambda t: records[t]['wins'], reverse=True)
            top_division_teams.append(sorted_division_teams[0])

        # Sort top division teams by wins
        sorted_top_division_teams = sorted(top_division_teams, key=lambda t: records[t]['wins'], reverse=True)

        # Sort remaining teams by wins in descending order
        remaining_teams = [team for team in conference_teams if team not in sorted_top_division_teams]
        sorted_remaining_teams = sorted(remaining_teams, key=lambda t: records[t]['wins'], reverse=True)

        # Combine top division teams and remaining teams to get top 7 teams
        top_teams = sorted_top_division_teams + sorted_remaining_teams[:3]

        # Apply the logic for seeds 5, 6, and 7 based on head-to-head matchups
        seeds_1_to_4 = top_teams[:4]
        seeds_5_to_7 = sorted(top_teams[4:], key=lambda t: records[t]['wins'], reverse=True)
        #seeds_5_to_7 = apply_tiebreakers(seeds_5_to_7)
        top_teams = seeds_1_to_4 + seeds_5_to_7

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

# Function to clear all winners and reset records
def clear_all_winners():
    for game in games:
        previous_winner = game.get('winner')
        if previous_winner:
            if previous_winner == game['team1']:
                records[game['team1']]['wins'] -= 1
                records[game['team2']]['losses'] -= 1
            else:
                records[game['team1']]['losses'] -= 1
                records[game['team2']]['wins'] -= 1

            # Update head-to-head
            if game['team1'] in records[game['team2']]['head_to_head']:
                records[game['team2']]['head_to_head'][game['team1']] -= 1
            if game['team2'] in records[game['team1']]['head_to_head']:
                records[game['team1']]['head_to_head'][game['team2']] -= 1

            # Record the outcome of the game
            if previous_winner == game['team1']:
                records[game['team1']]['outcomes'][game['team2']]['wins'] -= 1
                records[game['team2']]['outcomes'][game['team1']]['losses'] -= 1
            else:
                records[game['team2']]['outcomes'][game['team1']]['wins'] -= 1
                records[game['team1']]['outcomes'][game['team2']]['losses'] -= 1

            # Update division wins
            if 'division_game' in game and game['division_game']:
                if previous_winner == game['team1']:
                    records[game['team1']]['division_wins'] -= 1
                else:
                    records[game['team2']]['division_wins'] -= 1

            # Clear the winner
            game['winner'] = None

    # Save the updated game data
    save_game_data('games.json', {'teams': teams, 'games': games})

    # Restart the script
    root.destroy()  # Close the current Tkinter window
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Add a button to clear all winners
clear_winners_button = ttk.Button(root, text="Clear All Winners", command=clear_all_winners)
clear_winners_button.grid(row=2, column=1, sticky="e", padx=10, pady=10)

# Run the application
root.mainloop()