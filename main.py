from joblib import load
from model_prediction import predict_season_games, predict_wild_card_round, predict_divisional_round
from model_pipeline import run_model_variations
from model_prediction import predict_game_score
from model_training import train_model

# run_model_variations()

top_models_5 = [
    "model_2014_2023_unscaled_ridge_100_features_included",
    "model_2022_2023_unscaled_elasticnet_0.1_features_removed",
    "model_2022_2023_unscaled_lasso_0.01_features_included",
    "model_2022_2023_unscaled_ridge_10_features_included",
    "model_2022_2023_unscaled_elasticnet_100_features_included"
]

top_models_20 = model_names = [
    "model_2014_2023_unscaled_ridge_100_features_included",
    "model_2022_2023_unscaled_elasticnet_0.1_features_removed",
    "model_2022_2023_unscaled_lasso_0.01_features_included",
    "model_2022_2023_unscaled_ridge_10_features_included",
    "model_2022_2023_unscaled_elasticnet_100_features_included",
    "model_2022_2023_unscaled_ridge_0.1_features_included",
    "model_2014_2023_unscaled_lasso_0.01_features_included",
    "model_2022_2023_unscaled_lasso_0.1_features_included",
    "model_2022_2023_unscaled_ridge_1_features_included",
    "model_2014_2023_unscaled_elasticnet_0.1_features_included",
    "model_2019_2023_unscaled_elasticnet_0.1_features_included",
    "model_2022_2023_unscaled_ridge_0.01_features_included",
    "model_2014_2023_unscaled_ridge_10_features_included",
    "model_2014_2023_unscaled_elasticnet_0.01_features_included",
    "model_2014_2023_unscaled_ridge_0.01_features_included",
    "model_2022_2023_unscaled_ridge_0.01_features_removed",
    "model_2022_2023_unscaled_elasticnet_0.01_features_removed",
    "model_2022_2023_unscaled_none_0_features_removed",
    "model_2014_2023_unscaled_none_0_features_included",
    "model_2022_2023_unscaled_lasso_10_features_included"
]

top_models_50 = [
    "model_2014_2023_unscaled_ridge_100_features_included",
    "model_2022_2023_unscaled_elasticnet_0.1_features_removed",
    "model_2022_2023_unscaled_lasso_0.01_features_included",
    "model_2022_2023_unscaled_ridge_10_features_included",
    "model_2022_2023_unscaled_elasticnet_100_features_included",
    "model_2022_2023_unscaled_ridge_0.1_features_included",
    "model_2014_2023_unscaled_lasso_0.01_features_included",
    "model_2022_2023_unscaled_lasso_0.1_features_included",
    "model_2022_2023_unscaled_ridge_1_features_included",
    "model_2014_2023_unscaled_elasticnet_0.1_features_included",
    "model_2019_2023_unscaled_elasticnet_0.1_features_included",
    "model_2022_2023_unscaled_ridge_0.01_features_included",
    "model_2014_2023_unscaled_ridge_10_features_included",
    "model_2014_2023_unscaled_elasticnet_0.01_features_included",
    "model_2014_2023_unscaled_ridge_0.01_features_included",
    "model_2022_2023_unscaled_ridge_0.01_features_removed",
    "model_2022_2023_unscaled_elasticnet_0.01_features_removed",
    "model_2022_2023_unscaled_none_0_features_removed",
    "model_2014_2023_unscaled_none_0_features_included",
    "model_2022_2023_unscaled_lasso_10_features_included",
    "model_2022_2023_unscaled_ridge_0.1_features_removed",
    "model_2014_2023_unscaled_ridge_1_features_included",
    "model_2014_2023_unscaled_elasticnet_1_features_included",
    "model_2023_2023_unscaled_ridge_100_features_included",
    "model_2023_2023_unscaled_lasso_0.1_features_included",
    "model_2022_2023_unscaled_ridge_1_features_removed",
    "model_2022_2023_unscaled_elasticnet_10_features_included",
    "model_2022_2023_unscaled_lasso_0.01_features_removed",
    "model_2014_2023_unscaled_lasso_0.1_features_included",
    "model_2014_2023_unscaled_ridge_0.1_features_included",
    "model_2022_2023_unscaled_elasticnet_1_features_included",
    "model_2014_2023_unscaled_ridge_0.1_features_removed",
    "model_2022_2023_unscaled_ridge_100_features_removed",
    "model_2014_2023_unscaled_elasticnet_100_features_included",
    "model_2023_2023_unscaled_elasticnet_0.1_features_included",
    "model_2014_2023_unscaled_ridge_1_features_removed",
    "model_2014_2023_unscaled_ridge_0.01_features_removed",
    "model_2014_2023_unscaled_none_0_features_removed",
    "model_2019_2023_unscaled_elasticnet_1_features_included",
    "model_2014_2023_unscaled_lasso_10_features_included",
    "model_2023_2023_unscaled_elasticnet_0.01_features_included",
    "model_2023_2023_unscaled_ridge_0.1_features_included",
    "model_2014_2023_unscaled_elasticnet_0.01_features_removed",
    "model_2022_2023_unscaled_lasso_100_features_included",
    "model_2019_2023_unscaled_lasso_0.1_features_included",
    "model_2023_2023_unscaled_lasso_0.01_features_included",
    "model_2019_2023_unscaled_ridge_100_features_included",
    "model_2023_2023_unscaled_elasticnet_10_features_included",
    "model_2023_2023_unscaled_ridge_10_features_included",
    "model_2019_2023_unscaled_elasticnet_10_features_included"
]

top_scaled_models_5 = [
    "model_2019_2023_scaled_elasticnet_1_features_removed",
    "model_2023_2023_scaled_ridge_100_features_removed",
    "model_2022_2023_scaled_elasticnet_1_features_included",
    "model_2014_2023_scaled_elasticnet_1_features_removed",
    "model_2022_2023_scaled_elasticnet_0.1_features_included"
]


# predict_divisional_round(top_models_20, print_results=True)

# predict_wild_card_round(top_scaled_models_5)

train_model(
    start_year=2023,
    end_year=2023,
    model_name="model_2023_2023_scaled_ridge_1.0",
    use_scaling=True,
    regularization='ridge',
    alpha=1.0,
    remove_features=False
)

scaled_model = [
    "model_2023_2023_scaled_ridge_1.0"
]

predict_divisional_round(scaled_model)
