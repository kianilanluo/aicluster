
# Real Estate Price Prediction

This project is a Flask application that provides a machine learning model for predicting real estate prices based on various features such as location, property type, number of rooms, and more.

## Prerequisites

Before running this application, ensure that you have the following installed:

- Python 3.7 or later
- Docker
- Kubernetes (or a local Kubernetes environment like Minikube or Docker Desktop with Kubernetes enabled)

## Getting Started

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/real-estate-prediction.git
cd real-estate-prediction
```

### 2. Build the Docker image:

```bash
docker build -t real-estate-prediction:v1 .
```

### 3. Deploy the application to your Kubernetes cluster:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### 4. Verify that the deployment and service are running:

```bash
kubectl get deployments
kubectl get services
```

### 5. Find the external IP address of the LoadBalancer service:

```bash
kubectl get services
```

Look for the `EXTERNAL-IP` of the `real-estate-prediction` service.

### 6. Access the application using the external IP address and port 80:

```bash
http://<EXTERNAL-IP>:80/predict
```

Replace `<EXTERNAL-IP>` with the actual external IP address of your service.

## Usage

To predict the price of a real estate property, send a POST request to the `/predict` endpoint with the following JSON payload:

```bash
{
  curl -X POST -H "Content-Type: application/json" -d '{"avg_area_income": 79545.45, "avg_area_house_age": 5.98, "avg_area_num_rooms": 7.0, "avg_area_num_bedrooms": 4.0, "area_population": 23086.8}' http://localhost:80/predict
}
```
The API will respond with the predicted price for the given property features.

## Development

If you want to make changes to the Flask application code, follow these steps:

1. Update the Flask application code in the `realestatepriceprediction.py` file.

2. Rebuild the Docker image:

```bash
docker build -t real-estate-prediction:v1 .
```

3. Update the deployment in Kubernetes:

```bash
kubectl set image deployment/real-estate-prediction real-estate-prediction=real-estate-prediction:v1
```

This will update the deployment with the new Docker image without affecting the service or any other resources.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is not licensed.
