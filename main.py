from joblib import load
from model_prediction import predict_season_games, predict_wild_card_round, predict_divisional_round
from model_pipeline import run_model_variations
from model_prediction import predict_game_score
from model_training import train_model

run_model_variations()


# predict_divisional_round(top_models_20, print_results=True)

# predict_wild_card_round(top_scaled_models_5)



# predict_divisional_round(scaled_model)
