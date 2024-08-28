
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

## Kubernetes Deployment Configuration (Optional)

### 1. Using Local Docker Images

If you are running a local Kubernetes cluster (e.g., using `minikube` or `k3d`), and your Docker image is stored locally, you need to ensure that Kubernetes uses this local image rather than trying to pull it from a remote repository. To achieve this, follow these steps:

1. **Set `imagePullPolicy` to `Never`:**
   - In your `deployment.yaml` file, set the `imagePullPolicy` to `Never`. This will instruct Kubernetes to use the local image directly.

   ```yaml
   spec:
     containers:
     - name: real-estate-prediction
       image: real-estate-prediction:v2
       imagePullPolicy: Never
       ports:
       - containerPort: 5002
   ```

2. **Apply the Deployment:**
   - After making this change, apply your deployment using the following command:

   ```bash
   kubectl apply -f deployment.yaml
   ```

### 2. Using a Docker Registry

You need to ensure that Kubernetes can pull the image from this registry. Follow these steps:

1. **Tag and Push the Image:**
   - First, tag your Docker image with the registry URL and your username, and then push it to the registry.

   ```bash
   docker tag real-estate-prediction:v2 <your-registry-username>/real-estate-prediction:v2
   docker push <your-registry-username>/real-estate-prediction:v2
   ```

2. **Update the `deployment.yaml` File:**
   - In your `deployment.yaml` file, update the image name to include the registry URL.

   ```yaml
   spec:
     containers:
     - name: real-estate-prediction
       image: <your-registry-username>/real-estate-prediction:v2
       ports:
       - containerPort: 5002
   ```

3. **Apply the Deployment:**
   - Apply the updated deployment file:

   ```bash
   kubectl apply -f deployment.yaml
   ```

4. **(Optional) Handle Private Registries:**
   - If you are using a private registry, you need to create a Kubernetes secret to store your Docker credentials.

   ```bash
   kubectl create secret docker-registry regcred      --docker-server=<your-registry-server>      --docker-username=<your-username>      --docker-password=<your-password>      --docker-email=<your-email>
   ```

   - Then, update your `deployment.yaml` to use this secret:

   ```yaml
   spec:
     imagePullSecrets:
     - name: regcred
     containers:
     - name: real-estate-prediction
       image: <your-registry-username>/real-estate-prediction:v2
   ```

5. **Apply the Deployment:**
   - Apply the deployment again:

   ```bash
   kubectl apply -f deployment.yaml
   ```
## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is not licensed.