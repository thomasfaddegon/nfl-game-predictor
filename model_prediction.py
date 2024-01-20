import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import mean_squared_error
from sklearn.inspection import permutation_importance
from sklearn.preprocessing import StandardScaler
from feature_engineering import create_game_features
from utils import get_team_name
from joblib import dump
from joblib import load
import os

def predict_game_score(away_team, home_team, model, season=2023, print_results=False, remove_features=False):
    # Create game features
    home_features, away_features = create_game_features(home_team, away_team, season, remove_features=remove_features)

    # Predict the score
    home_score = model.predict(home_features)[0]
    away_score = model.predict(away_features)[0]

    if print_results:
        print(f'{away_team}: {away_score}')
        print(f'{home_team}: {home_score}')
        if home_score > away_score:
            print(f'The {home_team} win {round(home_score)} to {round(away_score)}!')
        else:
            print(f'The {away_team} win {round(away_score)} to {round(home_score)}!')
        print('')

    winner = home_team if home_score > away_score else away_team

    return winner, away_score, home_score


def predict_season_games(model, season=2023, remove_features=False):
    print('predicting games...')
    # Load the scores data and filter by season
    scores_df = pd.read_csv('data/scores.csv')
    filtered_scores_df = scores_df[(scores_df['season'] == season)].copy().reset_index(drop=True)

    # Convert team acronyms in scores data to full names
    filtered_scores_df['home_team'] = filtered_scores_df['home_team'].apply(get_team_name)
    filtered_scores_df['away_team'] = filtered_scores_df['away_team'].apply(get_team_name)


    pick_record = [0, 0]

    # Loop through each game and predict score
    for index, game in filtered_scores_df.iterrows():
        # print(f'{game["away_team"]} @ {game["home_team"]}')
        acutal_winner = game['away_team'] if game['away_score'] >= game['home_score'] else game['home_team']

        predicted_winner = predict_game_score(game['away_team'], game['home_team'], model, season, remove_features)

        if (predicted_winner[0] == acutal_winner):
            pick_record[0] += 1
        else:
            pick_record[1] += 1

    print(f'Picks: {pick_record[0]} - {pick_record[1]}')
    predict_percentage = round(pick_record[0] / (pick_record[0] + pick_record[1]) * 100, 2)
    print(f'Predicted {predict_percentage}% of games correctly!')

    return predict_percentage

def predict_wild_card_round (models):
    for model in models:
        predict_game_score('Browns', 'Texans', model, print_results=True)
        predict_game_score('Dolphins', 'Chiefs', model, print_results=True)
        predict_game_score('Steelers', 'Bills', model, print_results=True)
        predict_game_score('Packers', 'Cowboys',  model, print_results=True)
        predict_game_score('Rams', 'Lions', model, print_results=True)
        predict_game_score('Eagles', 'Buccaneers', model, print_results=True)

