import pandas as pd
from feature_engineering import create_game_features
from utils import get_team_name, remove_features_from_dataframe
from joblib import load
from sklearn.preprocessing import RobustScaler
import os


def predict_game_score(away_team, home_team, model_names=['model_2014_2023_unscaled_elasticnet_1_features_included'], season=2023, away_season_year=None, home_season_year=None, print_results=False, remove_features=False):

    away_season_year = away_season_year if away_season_year is not None else season
    home_season_year = home_season_year if home_season_year is not None else season

    # Predict the score for each model
    home_scores = []
    away_scores = []
    home_wins = 0
    away_wins = 0

    for model_name in model_names:
        remove_features = 'features_removed' in model_name
        is_scaled = 'unscaled' not in model_name


         # Create game features with or without feature removal
        home_features, away_features = create_game_features(home_team, away_team, home_season_year, away_season_year, remove_features=remove_features)


        print(home_features)
        print(away_features)

        if is_scaled:
            # Load the scaler
            scaler_path = f"models/scaler_{model_name}.joblib"
            scaler = load(scaler_path)

             # Apply scaling to features
            home_features_scaled = scaler.transform(home_features)
            away_features_scaled = scaler.transform(away_features)

            # Convert scaled arrays back to DataFrames with original feature names
            home_features = pd.DataFrame(home_features_scaled, columns=home_features.columns)
            away_features = pd.DataFrame(away_features_scaled, columns=away_features.columns)

        print(type(home_features), type(away_features))

        print(f"Shape of home_features: {home_features.shape}")
        print(f"Shape of away_features: {away_features.shape}")

        # Load the model

        model_path = f"models/{model_name}.joblib"
        loaded_model = load(model_path)

        home_score = loaded_model.predict(home_features)[0]
        away_score = loaded_model.predict(away_features)[0]

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
        print(f'{home_team} {round(sum(home_scores) / len(model_names))} - {away_team} {round(sum(away_scores) / len(model_names))}')

        print('Scores:')
        for i, model_name in enumerate(model_names):
            print(f'{model_name}: {home_team} {round(home_scores[i])}, {away_team} {round(away_scores[i])}')

    # Determine the winner based on average scores
    winner = home_team if round(sum(home_scores) / len(model_names)) > round(sum(away_scores) / len(model_names)) else away_team

    avg_home_score = round(sum(home_scores) / len(model_names))
    avg_away_score = round(sum(away_scores) / len(model_names))

    return winner, avg_home_score, avg_away_score


def predict_season_games(model_names, season=2023, remove_features=False, print_results=False):
    # print(f'predicting games for {season}')

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

        predicted_winner = predict_game_score(game['away_team'], game['home_team'], model_names, season, print_results=False, remove_features=remove_features)

        if (predicted_winner[0] == acutal_winner):
            pick_record[0] += 1
        else:
            pick_record[1] += 1

    predict_percentage = round(pick_record[0] / (pick_record[0] + pick_record[1]) * 100, 2)
    if print_results:
        print(f'Picks: {pick_record[0]} - {pick_record[1]}')
        print(f'Predicted {predict_percentage}% of games correctly!')

    return predict_percentage

def predict_wild_card_round (models, print_results):
    predict_game_score('Browns', 'Texans', models, print_results=True)
    predict_game_score('Dolphins', 'Chiefs', models, print_results=True)
    predict_game_score('Steelers', 'Bills', models, print_results=True)
    predict_game_score('Packers', 'Cowboys',  models, print_results=True)
    predict_game_score('Rams', 'Lions', models, print_results=True)
    predict_game_score('Eagles', 'Buccaneers', models, print_results=True)

def predict_divisional_round (models, print_results=False):
    predict_game_score('Texans', 'Ravens', models, print_results=True,)
    predict_game_score('Packers', '49ers', models, print_results=True,)
    predict_game_score('Buccaneers', 'Lions', models, print_results=True,)
    predict_game_score('Chiefs', 'Bills',  models, print_results=True,)

def predict_conference_championships (models, print_results=False):
    predict_game_score('Chiefs', 'Ravens', models, print_results=True,)
    predict_game_score('Lions', '49ers', models, print_results=True,)

def predict_super_bowl (models, print_results=False):
    predict_game_score('49ers', 'Chiefs', models, print_results=True,)

