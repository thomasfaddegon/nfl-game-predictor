import sys
print("Python Executable:", sys.executable)

from joblib import load
from model_prediction import predict_season_games, predict_super_bowl, predict_wild_card_round, predict_divisional_round, predict_conference_championships
from model_pipeline import run_model_variations
from model_prediction import predict_game_score
from model_training import train_model

# run_model_variations()


# predict_divisional_round(top_models_20, print_results=True)

# predict_wild_card_round(top_scaled_models_5)

top_models_10 = [
    "model_2022_2023_scaled_ridge_0.1_features_included",
    "model_2022_2023_unscaled_elasticnet_0.1_features_removed",
    "model_2014_2023_scaled_none_0_features_included",
    "model_2022_2023_unscaled_lasso_0.1_features_removed",
    "model_2014_2023_scaled_lasso_0.01_features_included",
    "model_2022_2023_scaled_elasticnet_1_features_included",
    "model_2022_2023_unscaled_ridge_10_features_included",
    "model_2014_2023_unscaled_ridge_100_features_included",
    "model_2022_2023_scaled_ridge_0.01_features_removed",
    "model_2022_2023_unscaled_none_0_features_removed"
    ]

best_model = "model_2022_2023_unscaled_ridge_1_features_included"


# predict_divisional_round(scaled_model)

predict_wild_card_round(top_models_10, print_results=True)

predict_super_bowl([best_model], print_results=True)