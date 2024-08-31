from prefect import flow, task
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os
os.chdir('/Users/kian/Desktop/Education/Dessertation/kian_dissertation')

@task
def load_data():
    """Load the housing dataset."""
    usa_housing = pd.read_csv('USA_Housing.xls')
    return usa_housing

@task
def preprocess_data(usa_housing):
    """Prepare the data for modeling."""
    X = usa_housing[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms', 
                     'Avg. Area Number of Bedrooms', 'Area Population']]
    y = usa_housing['Price']
    return X, y

@task
def train_model(X, y):
    """Train the linear regression model."""
    model = LinearRegression()
    model.fit(X, y)
    return model

@flow(name="Training Phase")
def training_phase():
    data = load_data()
    X, y = preprocess_data(data)
    model = train_model(X, y)
    return model

@task
def evaluate_model(model, X, y):
    """Evaluate the model performance."""
    y_pred = model.predict(X)
    mse = mean_squared_error(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    return mse, mae, r2

@flow(name="Model Evaluation")
def model_evaluation(model, X, y):
    mse, mae, r2 = evaluate_model(model, X, y)
    print(f"Model Evaluation: MSE={mse}, MAE={mae}, R2 Score={r2}")

# Run the flows
if __name__ == "__main__":
    data = load_data()
    X, y = preprocess_data(data)
    trained_model = training_phase()
    model_evaluation(trained_model, X, y)