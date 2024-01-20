import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import mean_squared_error
from sklearn.inspection import permutation_importance
from sklearn.preprocessing import StandardScaler
from utils import get_team_name, get_team_acronym
from joblib import dump
from joblib import load
import os



pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to next line

def load_and_clean_offense_defense_data (year):
    # Load the offense and defense data, rename the columns and drop unnecessary columns
    offense_passing_df = pd.read_csv(f'data/{year}/offense_passing_{year}.csv', index_col=0)
    offense_passing_df.columns = ['Offense_Passing_' + col for col in offense_passing_df.columns]
    offense_passing_df = offense_passing_df.drop('Offense_Passing_SACK YDS', axis=1)

    offense_rushing_df = pd.read_csv(f'data/{year}/offense_rushing_{year}.csv', index_col=0)
    offense_rushing_df.columns = ['Offense_Rushing_' + col for col in offense_rushing_df.columns]

    defense_passing_df = pd.read_csv(f'data/{year}/defense_passing_{year}.csv', index_col=0)
    defense_passing_df.columns = ['Defense_Passing_' + col for col in defense_passing_df.columns]
    defense_passing_df = defense_passing_df.drop('Defense_Passing_Unnamed: 2', axis=1)

    defense_rushing_df = pd.read_csv(f'data/{year}/defense_rushing_{year}.csv', index_col=0)
    defense_rushing_df.columns = ['Defense_Rushing_' + col for col in defense_rushing_df.columns]
    defense_rushing_df = defense_rushing_df.drop('Defense_Rushing_Unnamed: 2', axis=1)

    # Convert Time of Possession to seconds
    offense_rushing_df['Offense_Rushing_TOP'] = offense_rushing_df['Offense_Rushing_TOP'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]))
    defense_rushing_df['Defense_Rushing_TOP'] = defense_rushing_df['Defense_Rushing_TOP'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]))

    # Merge the offense and defense data
    offense_combined_df = pd.merge(offense_passing_df, offense_rushing_df, left_on='Offense_Passing_TEAM', right_on='Offense_Rushing_TEAM')
    defense_combined_df = pd.merge(defense_passing_df, defense_rushing_df, left_on='Defense_Passing_TEAM', right_on='Defense_Rushing_TEAM')

    return offense_combined_df, defense_combined_df

def create_game_features(home_team, away_team, offense_combined_df, defense_combined_df):
    # merge the data
    home_team_offense = offense_combined_df[offense_combined_df['Offense_Passing_TEAM'] == home_team]
    away_team_defense = defense_combined_df[defense_combined_df['Defense_Passing_TEAM'] == away_team]
    away_team_offense = offense_combined_df[offense_combined_df['Offense_Passing_TEAM'] == away_team]
    home_team_defense = defense_combined_df[defense_combined_df['Defense_Passing_TEAM'] == home_team]

    # Reset the index in place
    home_team_offense.reset_index(drop=True, inplace=True)
    away_team_defense.reset_index(drop=True, inplace=True)
    away_team_offense.reset_index(drop=True, inplace=True)
    home_team_defense.reset_index(drop=True, inplace=True)

    return home_team_offense, away_team_defense, away_team_offense, home_team_defense

def train_model(start_year, end_year, model_name, use_scaling=False, regularization=None, alpha=0.5, l1_ratio=0.5, remove_features=False):
    # Load the scores data
    scores_df = pd.read_csv('data/scores.csv')

    X = pd.DataFrame()

    for current_season in range(start_year, end_year + 1):
        print(f'Creating features for {current_season}...')
        # Filter scores by the current season
        season_scores_df = scores_df[scores_df['season'] == current_season].copy().reset_index(drop=True)

        # Convert team acronyms in scores data to full names
        season_scores_df['home_team'] = season_scores_df['home_team'].apply(get_team_name)
        season_scores_df['away_team'] = season_scores_df['away_team'].apply(get_team_name)

        # Load the offense and defense data for the current season
        offense_combined_df, defense_combined_df = load_and_clean_offense_defense_data(current_season)

        season_combined_features = []

        # Loop through each game and generate features
        for index, game in season_scores_df.iterrows():
            home_team_offense, away_team_defense, away_team_offense, home_team_defense = create_game_features(game['home_team'], game['away_team'], offense_combined_df, defense_combined_df)

            # Prepare new columns
            new_columns_df = pd.DataFrame({
                'game_id': [game['game_id']],
                'team_score': [game['home_score']],
                'is_home': [1],
            })

            # Combine home team offense with away team defense
            home_features = pd.concat([new_columns_df, home_team_offense, away_team_defense], axis=1)
            season_combined_features.append(home_features)

            # Update new_columns_df for away team
            new_columns_df['team_score'] = [game['away_score']]
            new_columns_df['is_home'] = [0]

            # Combine away team offense with home team defense
            away_features = pd.concat([new_columns_df, away_team_offense, home_team_defense], axis=1)
            season_combined_features.append(away_features)

        # Combine all the features for the season
        season_features = pd.concat(season_combined_features, ignore_index=True)

        # Define the features to remove if remove_features is True
        if remove_features:
            features_to_remove = ['Offense_Passing_PTS/G', 'Offense_Rushing_PTS/G',
                                  'Defense_Passing_SACK YDS', 'Offense_Passing_SACKS',
                                  'Defense_Passing_TD', 'Defense_Rushing_TOP', 'Defense_Rushing_ATT',
                                  'Offense_Passing_INT', 'Offense_Rushing_ATT', 'Offense_Rushing_YDS/ATT',
                                  'Offense_Rushing_TOP', 'Offense_Rushing_YDS']
            season_features = season_features.drop(columns=features_to_remove, errors='ignore')

        # Add the features for this season to the overall dataset
        X = pd.concat([X, season_features])

    X.to_csv('x.csv', index=False)

    # Remove team columns and game id
    X = X.drop(['Offense_Passing_TEAM', 'Offense_Rushing_TEAM', 'Defense_Passing_TEAM', 'Defense_Rushing_TEAM', 'game_id'], axis=1)

    # Create X and y
    y = X['team_score']
    X = X.drop('team_score', axis=1)

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Apply scaling if specified
    if use_scaling:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Convert scaled arrays back into DataFrames to prevent warnings
        X_train = pd.DataFrame(X_train_scaled, columns=X.columns)
        X_test = pd.DataFrame(X_test_scaled, columns=X.columns)
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Choose the model based on regularization type
    if regularization == 'ridge':
        model = Ridge(alpha=alpha)
    elif regularization == 'lasso':
        model = Lasso(alpha=alpha)
    elif regularization == 'elasticnet':
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio)
    else:
        model = LinearRegression()

    # Fit the model
    model.fit(X_train, y_train)

    # Predict and evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")

    # Save the model
    dump(model, f'models/{model_name}.joblib')

    return mse

def predict_game_score(away_team, home_team, model, season=2023, print_results=False, remove_features=False):


    # Load the offense and defense data for all teams
    offense_combined_df, defense_combined_df = load_and_clean_offense_defense_data(season)


    # Your main code block
    offense_combined_df, defense_combined_df = load_and_clean_offense_defense_data(season)
    home_team_offense, away_team_defense, away_team_offense, home_team_defense = create_game_features(home_team, away_team, offense_combined_df, defense_combined_df)

    # Explicitly create copies to stop warning
    home_team_offense = home_team_offense.copy()
    away_team_offense = away_team_offense.copy()

    # Add home column to copies
    home_team_offense.insert(0, 'is_home', 1)  # Adding 'is_home' as 1 for home team
    away_team_offense.insert(0, 'is_home', 0)  # Adding 'is_home' as 0 for away team

    # Remove team columns
    home_team_offense = home_team_offense.drop(['Offense_Passing_TEAM', 'Offense_Rushing_TEAM'], axis=1)
    away_team_offense = away_team_offense.drop(['Offense_Passing_TEAM', 'Offense_Rushing_TEAM'], axis=1)
    home_team_defense = home_team_defense.drop(['Defense_Passing_TEAM', 'Defense_Rushing_TEAM'], axis=1)
    away_team_defense = away_team_defense.drop(['Defense_Passing_TEAM', 'Defense_Rushing_TEAM'], axis=1)


    # Combine the stats to create a feature set for prediction
    home_features = pd.concat([home_team_offense, away_team_defense], axis=1)
    away_features = pd.concat([away_team_offense, home_team_defense], axis=1)

    # Check for NaN values in home_features and away_features before prediction and log them
    if home_features.isnull().values.any():
        print(home_team)
        nan_rows_home = home_features[home_features.isnull().any(axis=1)]
        print("Rows with NaN values in home_features:")
        print(nan_rows_home)

    if away_features.isnull().values.any():
        print(away_team)
        nan_rows_away = away_features[away_features.isnull().any(axis=1)]
        print("Rows with NaN values in away_features:")
        print(nan_rows_away)

    # Define the features to remove if remove_features is True
    if remove_features:
        features_to_remove = ['Offense_Passing_PTS/G', 'Offense_Rushing_PTS/G',
                              'Defense_Passing_SACK YDS', 'Offense_Passing_SACKS',
                              'Defense_Passing_TD', 'Defense_Rushing_TOP', 'Defense_Rushing_ATT',
                              'Offense_Passing_INT', 'Offense_Rushing_ATT', 'Offense_Rushing_YDS/ATT',
                              'Offense_Rushing_TOP', 'Offense_Rushing_YDS']

        home_features = home_features.drop(columns=features_to_remove, errors='ignore')
        away_features = away_features.drop(columns=features_to_remove, errors='ignore')

    # Predict the score
    home_score = model.predict(home_features)
    away_score = model.predict(away_features)

    home_score = home_score[0]
    away_score = away_score[0]

    if (print_results):
        print(f'{away_team}: {away_score}')
        print(f'{home_team}: {home_score}')
        if (home_score > away_score):
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

def display_all_models ():
    # List all files in the current working directory
    files_in_cwd = os.listdir(os.getcwd())

    # Filter for files that end with '.joblib'
    joblib_files = [file for file in files_in_cwd if file.endswith('.joblib')]

    print(sorted(joblib_files))

def run_model_variations(testing_year=2023):
    # Parameters
    year_ranges = [(2023 - years + 1, 2023) for years in [1, 2, 5, 10]]
    scale_options = [False, True]
    regularization_types = [None, 'ridge', 'lasso', 'elasticnet']
    regularization_strengths = [0.2, 0.4, 0.6, 0.8, 1.0]
    feature_removal_options = [False]

    results = []

    for start_year, end_year in year_ranges:
        for scale in scale_options:
            for reg_type in regularization_types:
                for alpha in regularization_strengths if reg_type else [None]:
                    for remove_features in feature_removal_options:
                        print(f"*** Model for {start_year} to {end_year} with scaling={scale}, reg={reg_type}, alpha={alpha}, features_removed={remove_features} ***")
                        # Model name based on configuration
                        model_name = f"model_{start_year}_{end_year}_{'scaled' if scale else 'unscaled'}_{reg_type or 'none'}_{alpha or ''}_{'features_removed' if remove_features else 'features_included'}"

                        # Train the model
                        mse = train_model(start_year, end_year, model_name, use_scaling=scale, regularization=reg_type, alpha=alpha, remove_features=remove_features)

                        model = load(f'models/{model_name}.joblib')

                        # Load the trained model and predict season games
                        accuracy = predict_season_games(model, testing_year)

                        # Store results
                        results.append({
                            'Start Year': start_year,
                            'End Year': end_year,
                            'Scaling': scale,
                            'Regularization': reg_type,
                            'Alpha': alpha,
                            'Features Removed': remove_features,
                            'MSE': mse,
                            'Accuracy': accuracy,
                            'Model Name': model_name
                        })

    # Convert results to DataFrame and sort
    results_df = pd.DataFrame(results)
    sorted_results = results_df.sort_values(by=['Accuracy', 'MSE'], ascending=[False, True])
    sorted_results.to_csv(f'results/results{testing_year}.csv', index=False)

    # Print or return the sorted results
    print(sorted_results)




run_model_variations(2023)
# run_model_variations(2022)
# run_model_variations(2021)


# # Create the model
# train_model(2014, 2023, 'finalized/model_2014_2023_false_ridge_unscaled', use_scaling=False, regularization=0.6, alpha=0.5, remove_features=False)


# train_model(2019, 2023, 'finalized/model_2019_2023_false_ridge_unscaled', use_scaling=False, regularization=0.6, alpha=0.5, remove_features=False)

# train_model(2023, 2023, 'finalized/model_2023_2023,false_ridge_unscaled', use_scaling=False, regularization=0.6, alpha=0.5, remove_features=False)


#  # Load the model
# model = load('models/finalized/model_2014_2023_false_ridge_unscaled.joblib')

# # predict_season_games(model, 2014)

# predict_wild_card_round(model)

#  # Load the model
# model = load('models/finalized/model_2019_2023_false_ridge_unscaled.joblib')

# # predict_season_games(model, 2014)

# predict_wild_card_round(model)

#  # Load the model
# model = load('models/finalized/model_2023_2023_false_ridge_unscaled.joblib')

# # predict_season_games(model, 2014)

# predict_wild_card_round(model)


# models
# trained_model_5.joblib
# trained_model_5_scaled.joblib
# trained_model_5_regularized.joblib
# trained_model_5_scaled_regularized.joblib


