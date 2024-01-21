from statistics import mean
import pandas as pd
from joblib import load
from model_training import train_model
from model_prediction import predict_season_games


def run_model_variations():
    # Parameters
    year_ranges = [(2023 - years + 1, 2023) for years in [1, 2, 5, 10]]
    scale_options = [False, True]
    regularization_types = [None, 'ridge', 'lasso', 'elasticnet']
    regularization_strengths = [0.01, 0.1, 1, 10, 100]
    feature_removal_options = [True, False]

    results = []

    for start_year, end_year in year_ranges:
        for scale in scale_options:
            for reg_type in regularization_types:
                for alpha in regularization_strengths if reg_type else [None]:
                    for remove_features in feature_removal_options:
                        print(f"*** Model for {start_year} to {end_year} with scaling={scale}, reg={reg_type}, alpha={alpha}, features_removed={remove_features} ***")

                        # Model name based on configuration
                        model_name = f"model_{start_year}_{end_year}_{'scaled' if scale else 'unscaled'}_{reg_type or 'none'}_{alpha or '0'}_{'features_removed' if remove_features else 'features_included'}"

                        # Train the model
                        mse, r_squared = train_model(start_year, end_year, model_name, use_scaling=scale, regularization=reg_type, alpha=alpha, remove_features=remove_features)

                        # Load the trained model and predict season games for last three years to determine accuracy
                        print('predicting games for the last 3 years...')
                        accuracy2021 = predict_season_games([model_name], 2021, remove_features=remove_features, print_results=False)
                        accuracy2022 = predict_season_games([model_name], 2022, remove_features=remove_features, print_results=False)
                        accuracy2023 = predict_season_games([model_name], 2023, remove_features=remove_features, print_results=False)
                        average_accuracy = mean([accuracy2021, accuracy2022, accuracy2023])
                        print(f'Average accuracy: {average_accuracy}')


                        # Store results
                        results.append({
                            'Start Year': start_year,
                            'End Year': end_year,
                            'Scaling': scale,
                            'Regularization': reg_type,
                            'Alpha': alpha,
                            'Features Removed': remove_features,
                            'MSE': mse,
                            'R-Squared': r_squared,
                            'Accuracy': average_accuracy,
                            'Model Name': model_name
                        })

    # Convert results to DataFrame and sort
    results_df = pd.DataFrame(results)
    sorted_results = results_df.sort_values(by=['Accuracy', 'MSE'], ascending=[False, True])
    sorted_results.to_csv(f'results/results_2021_2023.csv', index=False)

    # Print or return the sorted results
    # print(sorted_results)