import sys
from model_prediction import predict_game_score
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return "NFL Playoff Predictor API"

# More routes go here
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    away_team = data.get('away_team')
    home_team = data.get('home_team')
    predictions = predict_game_score(away_team, home_team,  season=2023, print_results=False, remove_features=False)
    return {"predictions": predictions}



if __name__ == '__main__':
    app.run(debug=True)
