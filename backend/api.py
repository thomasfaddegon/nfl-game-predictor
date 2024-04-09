from model_prediction import predict_game_score
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

# Determine CORS origins based on the environment
# def get_cors_origins():
#     # set production as default if it isn't already set
#     flask_env = os.environ.get('FLASK_ENV', 'development')
#     print('FLASK_ENV:', flask_env)
#     # Allow all origins in development
#     if flask_env == 'development':
#         return "*"
#     else:
#         return os.environ.get('CORS_ORIGINS')

# CORS(app, origins=get_cors_origins())

port = int(os.environ.get('PORT', 9090))

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api')
def index():
    return "You've reached the NFL Playoff Predictor API"

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    print('data: ', data)
    print('predicting...')
    away_team = data.get('awayTeam')
    away_year = data.get('awayYear')
    home_team = data.get('homeTeam')
    home_year = data.get('homeYear')

    # print(f'away_team: {away_team}, away_year: {away_year}, home_team: {home_team}, home_year: {home_year}')

    predictions = predict_game_score(away_team, home_team, model_names=['model_2014_2023_scaled_lasso_0.1_features_included'], away_season_year=away_year, home_season_year=home_year)

    print(predictions)

    return jsonify({"predictions": predictions})

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "Test endpoint reached"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'False') == 'True')

