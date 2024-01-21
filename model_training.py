import pandas as pd
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from utils import get_team_name, remove_features_from_dataframe
from joblib import dump
from feature_engineering import create_game_features

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

        season_combined_features = []

        # Loop through each game and generate features
        for _, game in season_scores_df.iterrows():
            # Use the updated create_game_features function
            home_features, away_features = create_game_features(game['home_team'], game['away_team'], current_season, remove_features)

            # Prepare new columns
            home_features['game_id'] = game['game_id']
            home_features['team_score'] = game['home_score']
            home_features['is_home'] = 1

            away_features['game_id'] = game['game_id']
            away_features['team_score'] = game['away_score']
            away_features['is_home'] = 0

            # Append to the combined features
            season_combined_features.append(home_features)
            season_combined_features.append(away_features)

        # Combine all the features for the season
        season_features = pd.concat(season_combined_features, ignore_index=True)


    # Optional: Save the features to a file
    # X.to_csv('x.csv', index=False)

    # Define the features to remove if remove_features is True
    if remove_features:
        season_features = remove_features_from_dataframe(season_features)

    # Create X
    X = pd.concat([X, season_features])

    # Remove game_id column
    X = X.drop(['game_id'], axis=1)


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

    r_squared = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse}")
    print(f"R^2: {r_squared}")

    # Save the model
    dump(model, f'models/{model_name}.joblib')

    return mse, r_squared