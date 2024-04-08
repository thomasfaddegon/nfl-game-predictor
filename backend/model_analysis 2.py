import joblib
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet

# Load the pre-trained model
model = joblib.load('models/model_2022_2023_scaled_ridge_0.1_features_included.joblib')

# Print or visualize feature importance
if isinstance(model, LinearRegression) or isinstance(model, Ridge) or isinstance(model, Lasso) or isinstance(model, ElasticNet):
    print("Coefficients (Feature Importance):")
    # Assuming your model has the attribute 'coef_' for accessing feature coefficients
    if hasattr(model, 'coef_'):
        for feature, coef in zip(range(len(model.coef_)), model.coef_):
            print(f"Feature {feature}: {coef}")
    else:
        print("Model does not have attribute 'coef_' for feature importance analysis.")
