import pandas as pd

def get_potential_winners(game_id, df):
    # Find the game row based on game_id
    game = df[df['id'] == game_id].iloc[0]

    # If the game has a winner, return the winner
    if pd.notna(game['winner_team']):
        return [game['winner_team']]

    # If the game is in round 1, return both teams
    if game['round'] == 1:
        return [team for team in [game['team1'], game['team2']] if pd.notna(team)]

    # Otherwise, find the two games that lead to this game
    previous_games = df[df['winner_goes_to_game'] == game_id]
    potential_winners = []

    # Recursively call this function on the previous games
    for prev_game_id in previous_games['id']:
        potential_winners.extend(get_potential_winners(prev_game_id, df))

    return potential_winners

# Load the CSV file
df = pd.read_csv('games.csv')

# potential_winners = get_potential_winners(63, df)
# print(potential_winners)


for game_id in range(1, 64):
    potential_winners = get_potential_winners(game_id, df)
    print(f"Game ID: {game_id}, Potential Winners: {potential_winners}")
