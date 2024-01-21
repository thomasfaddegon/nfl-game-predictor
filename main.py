from joblib import load
from model_prediction import predict_season_games, predict_wild_card_round, predict_divisional_round
from model_pipeline import run_model_variations
from model_prediction import predict_game_score
from model_training import train_model

run_model_variations(2021)
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

# predict_game_score('Ste"elers', 'Bills', top_models, 2023, print_results=True)

# predict_wild_card_round(top_models)



# train_model(2023, 2023, 'finalized/model_2023_2023,false_ridge_unscaled_removed', use_scaling=False, regularization=0.6, alpha=0.5, remove_features=True)

# predict_divisional_round(['finalized/model_2023_2023,false_ridge_unscaled_removed'], remove_features=True)


 # Load the model
# model = load('models/finalized/model_2014_2023_false_ridge_unscaled.joblib')
# predict_wild_card_round(model)

# model = load('models/finalized/model_2019_2023_false_ridge_unscaled.joblib')
# predict_wild_card_round(model)

#  # Load the model
# model = load('models/finalized/model_2019_2023_false_ridge_unscaled.joblib')

# # predict_season_games(model, 2014)

# predict_wild_card_round(model)

#  # Load the model
# model = load('models/finalized/model_2023_2023_false_ridge_unscaled.joblib')

# # predict_season_games(model, 2014)

# predict_wild_card_round(model)