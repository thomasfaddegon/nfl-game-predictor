from model_prediction import predict_game_score
from flask import Flask, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/api')
def index():
    return "NFL Playoff Predictor API"

# More routes go here
@app.route('/api/predict', methods=['POST'])
def predict():
    print('predicting...')
    data = request.json
    print(data)
    away_team = data.get('awayTeam')
    home_team = data.get('homeTeam')
    print('away: ', away_team)
    print('home: ', home_team)
    predictions = predict_game_score(away_team, home_team,  season=2023, print_results=True, remove_features=False)

    return {"predictions": predictions}



if __name__ == '__main__':
    app.run(debug=True)
