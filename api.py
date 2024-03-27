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
    print('predicting...')
    data = request.json
    away_team = data.get('awayTeam')
    home_team = data.get('homeTeam')
    print(f'away: {away_team}, home: {home_team}')

    predictions = predict_game_score(away_team, home_team,  season=2023, print_results=True, remove_features=False)

    print(predictions)

    return jsonify({"predictions": predictions})

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "Test endpoint reached"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)

