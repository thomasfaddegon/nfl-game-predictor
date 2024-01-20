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

def predict_game_score(away_team, home_team, models, season=2023, print_results=False, remove_features=False):
    print('running prediction...')
    # Create game features
    home_features, away_features = create_game_features(home_team, away_team, season, remove_features=remove_features)

    # Predict the score for each model
    home_scores = []
    away_scores = []
    home_wins = 0
    away_wins = 0

    for i, model in enumerate(models):
        model_path = f"models/{model}.joblib"
        model = load(model_path)
        print(model_path, os.path.exists(model_path))

        home_score = model.predict(home_features)[0]
        away_score = model.predict(away_features)[0]
        home_scores.append(home_score)
        away_scores.append(away_score)

        if home_score > away_score:
            home_wins += 1
        else:
            away_wins += 1

    if print_results:
        print('Games Won:')
        print(f'{home_team} {home_wins} - {away_team} {away_wins}')

        print('Avg Score:')
        print(f'{home_team} {round(sum(home_scores) / len(models))} - {away_team} {round(sum(away_scores) / len(models))}')

        print('Scores:')
        for i, model_name in enumerate(models):
            print(f'{model_name}: {home_team} {round(home_scores[i])}, {away_team} {round(away_scores[i])}')

    # Determine the winner based on average scores
    winner = home_team if round(sum(home_scores) / len(models)) > round(sum(away_scores) / len(models)) else away_team

    return winner, home_scores, away_scores


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
    predict_game_score('Browns', 'Texans', models, print_results=True)
    predict_game_score('Dolphins', 'Chiefs', models, print_results=True)
    predict_game_score('Steelers', 'Bills', models, print_results=True)
    predict_game_score('Packers', 'Cowboys',  models, print_results=True)
    predict_game_score('Rams', 'Lions', models, print_results=True)
    predict_game_score('Eagles', 'Buccaneers', models, print_results=True)

def predict_divisional_round (models, remove_features=False):
    predict_game_score('Texans', 'Ravens', models, print_results=True, remove_features=remove_features)
    predict_game_score('Packers', '49ers', models, print_results=True, remove_features=remove_features)
    predict_game_score('Buccaneers', 'Lions', models, print_results=True, remove_features=remove_features)
    predict_game_score('Chiefs', 'Bills',  models, print_results=True, remove_features=remove_features)


