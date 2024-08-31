import os
import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify

# Directory for storing the CSV files
DATA_DIR = 'content/'
MODEL_PATH = 'linear_regression_model.pkl'
SCALER_PATH = 'scaler.pkl'
PROCESSED_FILES_PATH = 'processed_files.txt'

def load_data_from_directory(directory, processed_files):
    """Load all new CSV files from a specified directory that have not been processed."""
    all_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    new_files = [f for f in all_files if f not in processed_files]

    if not new_files:
        return None, processed_files

    df_list = [pd.read_csv(os.path.join(directory, file)) for file in new_files]
    combined_df = pd.concat(df_list, ignore_index=True)

    processed_files.update(new_files)

    return combined_df, processed_files

def save_processed_files(processed_files):
    """Save the processed files list to a text file."""
    with open(PROCESSED_FILES_PATH, 'w') as f:
        for file in processed_files:
            f.write(f"{file}\n")

def load_processed_files():
    """Load the processed files list from a text file."""
    if os.path.exists(PROCESSED_FILES_PATH):
        with open(PROCESSED_FILES_PATH, 'r') as f:
            processed_files = set(f.read().splitlines())
    else:
        processed_files = set()

    return processed_files

def train_model_with_new_data(new_data, model=None, scaler=None):
    """Train or update the model with new data."""
    X = new_data[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms', 'Avg. Area Number of Bedrooms', 'Area Population']]
    y = new_data['Price']

    if scaler is None:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = scaler.transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.4, random_state=101)

    if model is None:
        model = LinearRegression()
        model.fit(X_train, y_train)
    else:
        model.fit(X_train, y_train)

    # Evaluate the model and show performance metrics
    evaluate_model(model, X_test, y_test)

    return model, scaler

def evaluate_model(model, X_test, y_test):
    """Evaluate the model and print performance metrics."""
    y_pred = model.predict(X_test)
    print("y_pred.shape: ", y_pred.shape)

    for actual, predicted in zip(y_test[:5], y_pred[:5]):
        print(f"Actual: {actual:.2f}, Predicted: {predicted:.2f}")

    print("Mean Absolute Error (MAE): ", mean_absolute_error(y_test, y_pred))
    print("Mean Squared Error (MSE): ", mean_squared_error(y_test, y_pred))
    print("Root Mean Squared Error (RMSE): ", np.sqrt(mean_squared_error(y_test, y_pred)))
    print("R-squared (R²) score: ", r2_score(y_test, y_pred))

    # Plot the actual vs. predicted prices
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=3)
    plt.xlabel("Actual Price")
    plt.ylabel("Predicted Price")
    plt.title("Actual vs. Predicted Prices")
    plt.show()

    # Plot the residuals
    residuals = y_test - y_pred
    plt.figure(figsize=(10, 6))
    plt.scatter(y_pred, residuals, alpha=0.5)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel("Predicted Price")
    plt.ylabel("Residuals")
    plt.title("Residuals vs. Predicted Prices")
    plt.show()

def load_model_and_scaler():
    """Load the model and scaler if they exist."""
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
    else:
        model = None
        scaler = None
    return model, scaler

def save_model_and_scaler(model, scaler):
    """Save the model and scaler."""
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

# Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        try:
            data = request.get_json()
            avg_area_income = data['avg_area_income']
            avg_area_house_age = data['avg_area_house_age']
            avg_area_num_rooms = data['avg_area_num_rooms']
            avg_area_num_bedrooms = data['avg_area_num_bedrooms']
            area_population = data['area_population']

            input_data = np.array([[avg_area_income, avg_area_house_age, avg_area_num_rooms, avg_area_num_bedrooms, area_population]])
            input_data_scaled = scaler.transform(input_data)

            predicted_price = model.predict(input_data_scaled)[0]

            return jsonify({'predicted_price': predicted_price})
        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        return jsonify({'message': 'Please send a POST request with the required housing metrics to get the predicted price.'})

def main():
    global model, scaler

    # Load processed files list
    processed_files = load_processed_files()

    # Load new data
    new_data, processed_files = load_data_from_directory(DATA_DIR, processed_files)

    if new_data is not None:
        print(f"Training with new data from {len(processed_files)} files...")
        # Train or update model with new data
        model, scaler = train_model_with_new_data(new_data, model, scaler)

        # Save the updated model and scaler
        save_model_and_scaler(model, scaler)

        # Save the processed files list
        save_processed_files(processed_files)
    else:
        print("No new data to process.")

if __name__ == '__main__':
    # Load the existing model and scaler
    model, scaler = load_model_and_scaler()

    # Train and evaluate the model
    main()

    # Start the Flask app
    app.run(host='0.0.0.0', port=5002, debug=True)
