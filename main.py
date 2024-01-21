from joblib import load
from model_prediction import predict_season_games, predict_wild_card_round, predict_divisional_round
from model_pipeline import run_model_variations
from model_prediction import predict_game_score
from model_training import train_model

# run_model_variations(2021)
# run_model_variations(2022)
# run_model_variations(2021)

top_models = [
    "model_2022_2023_unscaled_ridge_0.4_features_included",
    "model_2022_2023_unscaled_ridge_0.2_features_included",
    "model_2022_2023_unscaled_none__features_included",
    "model_2022_2023_unscaled_ridge_0.6_features_included",
    "model_2022_2023_unscaled_ridge_1.0_features_included",
    "model_2022_2023_unscaled_ridge_0.8_features_included",
    "model_2022_2023_unscaled_lasso_0.2_features_included",
    "model_2022_2023_unscaled_elasticnet_0.4_features_included",
    "model_2022_2023_unscaled_elasticnet_0.2_features_included",
    "model_2014_2023_unscaled_ridge_1.0_features_included"
]




train_model(2023, 2023, "model_2014_2023_unscaled_ridge_1.0_features_included", use_scaling=False, regularization="ridge", alpha=1.0, l1_ratio=0.5, remove_features=False)