import pandas as pd
from joblib import load
from model_training import train_model
from model_prediction import predict_season_games


def run_model_variations(testing_year=2023):
    # Parameters
    year_ranges = [(2023 - years + 1, 2023) for years in [1, 2, 5, 10]]
    scale_options = [False, True]
    regularization_types = [None, 'ridge', 'lasso', 'elasticnet']
    regularization_strengths = [0.2, 0.4, 0.6, 0.8, 1.0]
    feature_removal_options = [False]

    results = []

    for start_year, end_year in year_ranges:
        for scale in scale_options:
            for reg_type in regularization_types:
                for alpha in regularization_strengths if reg_type else [None]:
                    for remove_features in feature_removal_options:
                        print(f"*** Model for {start_year} to {end_year} with scaling={scale}, reg={reg_type}, alpha={alpha}, features_removed={remove_features} ***")

                        # Model name based on configuration
                        model_name = f"model_{start_year}_{end_year}_{'scaled' if scale else 'unscaled'}_{reg_type or 'none'}_{alpha or ''}_{'features_removed' if remove_features else 'features_included'}"

                        # Train the model
                        mse = train_model(start_year, end_year, model_name, use_scaling=scale, regularization=reg_type, alpha=alpha, remove_features=remove_features)

                        # model = load(f'models/{model_name}.joblib')

                        # Load the trained model and predict season games
                        accuracy = predict_season_games([model_name], testing_year, remove_features=remove_features)

                        # Store results
                        results.append({
                            'Start Year': start_year,
                            'End Year': end_year,
                            'Scaling': scale,
                            'Regularization': reg_type,
                            'Alpha': alpha,
                            'Features Removed': remove_features,
                            'MSE': mse,
                            'Accuracy': accuracy,
                            'Model Name': model_name
                        })

    # Convert results to DataFrame and sort
    results_df = pd.DataFrame(results)
    sorted_results = results_df.sort_values(by=['Accuracy', 'MSE'], ascending=[False, True])
    sorted_results.to_csv(f'results/results{testing_year}.csv', index=False)

    # Print or return the sorted results
    # print(sorted_results)