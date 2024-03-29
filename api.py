from model_prediction import predict_game_score
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins=["*"])

@app.route('/api')
def index():
    return "You've reached the NFL Playoff Predictor API"

# More routes go here
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    print('data: ', data)
    print('predicting...')
    away_team = data.get('awayTeam')
    away_year = data.get('awayYear')
    home_team = data.get('homeTeam')
    home_year = data.get('homeYear')

    print(f'away_team: {away_team}, away_year: {away_year}, home_team: {home_team}, home_year: {home_year}')

    predictions = predict_game_score(away_team, home_team, model_names=['model_2014_2023_scaled_lasso_0.01_features_included'], away_season_year=away_year, home_season_year=home_year)

    print(predictions)

    return jsonify({"predictions": predictions})

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "Test endpoint reached"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)

