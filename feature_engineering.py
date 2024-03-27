import pandas as pd
from data_processing import load_and_clean_offense_defense_data
from utils import remove_features_from_dataframe

def create_game_features(home_team, away_team, season, remove_features=False):
    # Load and clean offense and defense data
    offense_combined_df, defense_combined_df = load_and_clean_offense_defense_data(season)

    # Merge the data
    home_team_offense = offense_combined_df[offense_combined_df['Offense_Passing_TEAM'] == home_team]
    away_team_defense = defense_combined_df[defense_combined_df['Defense_Passing_TEAM'] == away_team]
    away_team_offense = offense_combined_df[offense_combined_df['Offense_Passing_TEAM'] == away_team]
    home_team_defense = defense_combined_df[defense_combined_df['Defense_Passing_TEAM'] == home_team]

    # Reset the index in place
    home_team_offense.reset_index(drop=True, inplace=True)
    away_team_defense.reset_index(drop=True, inplace=True)
    away_team_offense.reset_index(drop=True, inplace=True)
    home_team_defense.reset_index(drop=True, inplace=True)

    # Make copies to avoid SettingWithCopyWarning
    home_team_offense = home_team_offense.copy()
    home_team_defense = home_team_defense.copy()
    away_team_offense = away_team_offense.copy()
    away_team_defense = away_team_defense.copy()

    # Add 'is_home' column
    home_team_offense.insert(0, 'is_home', 1)
    away_team_offense.insert(0, 'is_home', 0)

    # Remove team columns without inplace=True and assign to new variables
    home_team_offense_final = home_team_offense.drop(['Offense_Passing_TEAM', 'Offense_Rushing_TEAM'], axis=1)
    away_team_offense_final = away_team_offense.drop(['Offense_Passing_TEAM', 'Offense_Rushing_TEAM'], axis=1)
    home_team_defense_final = home_team_defense.drop(['Defense_Passing_TEAM', 'Defense_Rushing_TEAM'], axis=1)
    away_team_defense_final = away_team_defense.drop(['Defense_Passing_TEAM', 'Defense_Rushing_TEAM'], axis=1)

    # Combine the stats to create a feature set for prediction
    home_features = pd.concat([home_team_offense_final, away_team_defense_final], axis=1)
    away_features = pd.concat([away_team_offense_final, home_team_defense_final], axis=1)

    # Check for NaN values and log them
    if home_features.isnull().values.any():
        print(f"NaN values found in features for {home_team}")
        nan_rows_home = home_features[home_features.isnull().any(axis=1)]
        print("Rows with NaN values in home_features:")
        print(nan_rows_home)

    if away_features.isnull().values.any():
        print(f"NaN values found in features for {away_team}")
        nan_rows_away = away_features[away_features.isnull().any(axis=1)]
        print("Rows with NaN values in away_features:")
        print(nan_rows_away)

    # Remove specified features
    if remove_features:
        home_features = remove_features_from_dataframe(home_features)
        away_features = remove_features_from_dataframe(away_features)

    return home_features, away_features
