from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import werkzeug

# Load the dataset
usa_housing = pd.read_csv('USA_Housing.xls')

# Prepare the data
X = usa_housing[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms', 'Avg. Area Number of Bedrooms', 'Area Population']]
y = usa_housing['Price']

# Train the model
model = LinearRegression()
model.fit(X, y)

app = Flask(__name__)

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        data = request.get_json()
        avg_area_income = data['avg_area_income']
        avg_area_house_age = data['avg_area_house_age']
        avg_area_num_rooms = data['avg_area_num_rooms']
        avg_area_num_bedrooms = data['avg_area_num_bedrooms']
        area_population = data['area_population']

        input_data = np.array([[avg_area_income, avg_area_house_age, avg_area_num_rooms, avg_area_num_bedrooms, area_population]])
        predicted_price = model.predict(input_data)[0]

        return jsonify({'predicted_price': predicted_price})
    else:
        return jsonify({'message': 'Please send a POST request with the required housing metrics to get the predicted price.'})


def main():
    if werkzeug.serving.is_running_from_reloader():
        return

    print("Length of Dataset: ", len(usa_housing))
    print("Shape of Dataset:", usa_housing.shape)

    usa_housing.head(5)

    from sklearn.model_selection import train_test_split

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=101)

    X_train.shape, y_train.shape, X_test.shape, y_test.shape

    # Train the model
    lm = LinearRegression()
    lm.fit(X_train, y_train)

    # Make prediction on the test set
    y_pred = lm.predict(X_test)
    print("y_pred.shape: ", y_pred.shape)

    for d in zip(y_test[:5], y_pred[:5]):
        print(f"Actual: {d[0]:.2f}, Predicted: {d[1]:.2f}")

    # Evaluate the model
    print("mean absolute error (MAE): ", mean_absolute_error(y_test, y_pred))
    print("mean squared error (MSE): ", mean_squared_error(y_test, y_pred))
    print("root mean squared error (RMSE): ", np.sqrt(mean_squared_error(y_test, y_pred)))
    print("R-squared (R^2) score: ", r2_score(y_test, y_pred))

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

if __name__ == '__main__':
    main()
    app.run(host='0.0.0.0', port=5002, debug=True)