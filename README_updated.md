
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

## Kubernetes Deployment Configuration

### 1. Ingress Controller Setup

To expose your `real-estate-prediction` service with SSL/TLS using an NGINX Ingress controller, follow these steps:

#### Step 1: Install NGINX Ingress Controller

1. **Install via Helm (Recommended):**

   ```bash
   helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
   helm repo update
   helm install ingress-nginx ingress-nginx/ingress-nginx
   ```

2. **Install using Kubernetes manifests:**

   ```bash
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
   ```

#### Step 2: Create Ingress Resource

1. Add the `ingress.yaml` file to your project:

   ```yaml
   # ingress.yaml
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: real-estate-ingress
     annotations:
       nginx.ingress.kubernetes.io/rewrite-target: /
       nginx.ingress.kubernetes.io/ssl-redirect: "true"
   spec:
     rules:
     - host: realestate.local
       http:
         paths:
         - path: /
           pathType: Prefix
           backend:
             service:
               name: real-estate-prediction
               port:
                 number: 80
     tls:
     - hosts:
       - realestate.local
       secretName: realestate-tls
   ```

2. Apply the `ingress.yaml`:

   ```bash
   kubectl apply -f ingress.yaml
   ```

#### Step 3: Set Up SSL/TLS

- **For local development (self-signed certificate):**

   Generate a self-signed certificate and create the Kubernetes secret:

   ```bash
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=realestate.local/O=local"
   kubectl create secret tls realestate-tls --key tls.key --cert tls.crt
   ```

- **For production (Let's Encrypt):**

   1. Install cert-manager:

      ```bash
      kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.7.1/cert-manager.yaml
      ```

   2. Add the `cluster-issuer.yaml` to your project and apply it:

      ```bash
      kubectl apply -f cluster-issuer.yaml
      ```

   3. Update `ingress.yaml` to use Let's Encrypt (as shown above).

#### Step 4: Apply Network Policy

1. Add the `network-policy.yaml` to your project:

   ```yaml
   # network-policy.yaml
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: allow-only-nginx
     namespace: default
   spec:
     podSelector:
       matchLabels:
         app: real-estate-prediction
     ingress:
     - from:
       - podSelector:
           matchLabels:
             app.kubernetes.io/name: ingress-nginx
       ports:
       - protocol: TCP
         port: 80
   ```

2. Apply the network policy:

   ```bash
   kubectl apply -f network-policy.yaml
   ```

### 2. Using Local Docker Images

If you are running a local Kubernetes cluster (e.g., using Docker Desktop, Minikube), and your Docker image is stored locally, ensure that Kubernetes uses the local image by setting `imagePullPolicy` to `Never`:

```yaml
spec:
  containers:
  - name: real-estate-prediction
    image: real-estate-prediction:v2
    imagePullPolicy: Never
    ports:
    - containerPort: 5002
```

### 3. Using a Docker Registry

For a production environment, where your image is stored in a Docker registry, follow these steps:

1. **Tag and Push the Image:**

   ```bash
   docker tag real-estate-prediction:v2 <your-registry-username>/real-estate-prediction:v2
   docker push <your-registry-username>/real-estate-prediction:v2
   ```

2. **Update `deployment.yaml`:**

   ```yaml
   spec:
     containers:
     - name: real-estate-prediction
       image: <your-registry-username>/real-estate-prediction:v2
       ports:
       - containerPort: 5002
   ```

3. **Apply the deployment:**

   ```bash
   kubectl apply -f deployment.yaml
   ```


## Configure Jenkins

To deploy this project using Jenkins, follow these steps:

### 1. Install Jenkins
If you don't already have Jenkins installed, you can install it using Docker:

```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
```

After Jenkins is up and running, access it by navigating to `http://localhost:8080` in your web browser. Complete the setup process by following the on-screen instructions.

### 2. Install Required Plugins
Make sure the following plugins are installed in Jenkins:
- Git Plugin
- Docker Plugin
- Kubernetes CLI Plugin
- Credentials Binding Plugin

You can install these plugins by navigating to `Manage Jenkins -> Manage Plugins -> Available`.

### 3. Set Up Jenkins Credentials
You will need to add the following credentials in Jenkins:

1. **GitHub Credentials**:
    - Go to `Manage Jenkins -> Manage Credentials`.
    - Add a new "Username with password" credential with the ID `github` (or modify the pipeline script if you choose a different ID).

2. **Kubeconfig File**:
    - Add a new "Secret file" credential for the kubeconfig file, with the ID `kubeconfig`.

### 4. Create a Jenkins Pipeline

1. Go to `Jenkins -> New Item`.
2. Select "Pipeline" and give your project a name.
3. In the "Pipeline" section, choose "Pipeline script" and paste the following script:

```groovy
pipeline {
    agent any

    environment {
        GITHUB_CREDENTIALS_ID = 'github'
        REPO_URL = 'Your repository'
        IMAGE_NAME = 'the image you created'
        DOCKER_PATH = '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin' // In Mac os
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    git branch: 'main', credentialsId: "${env.GITHUB_CREDENTIALS_ID}", url: "${env.REPO_URL}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    withEnv(["PATH+DOCKER=${env.DOCKER_PATH}"]) {
                        sh "docker build -t ${env.IMAGE_NAME} ."
                    }
                }
            }
        }

        stage('Deploy to Docker Desktop') {
            steps {
                script {
                    // Map container's port 80 to host's port 8081
                    sh "docker run -d -p 8081:80 ${env.IMAGE_NAME}"
                }
            }
        }

        stage('Start Local Docker Registry') {
            steps {
                script {
                    def registryRunning = sh(script: "docker ps | grep registry", returnStatus: true) == 0
                    if (!registryRunning) {
                        sh "docker run -d -p 5001:5000 --name registry registry:2"
                    }
                }
            }
        }

        stage('Push Docker Image to Local Registry') {
            steps {
                script {
                    sh "docker tag ${env.IMAGE_NAME} localhost:5001/${env.IMAGE_NAME}"
                    sh "docker push localhost:5001/${env.IMAGE_NAME}"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Use the kubeconfig credentials file from Jenkins
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                        sh """
                            kubectl --kubeconfig=${KUBECONFIG} apply -f deployment.yaml
                            kubectl --kubeconfig=${KUBECONFIG} apply -f service.yaml
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                sh 'docker system prune -f'
            }
        }
    }
}
```

### 5. Run the Jenkins Pipeline
- Click on "Build Now" to run the pipeline. 
- Monitor the console output to ensure that each stage is executed correctly.
- The pipeline will automatically check out the code from your GitHub repository, build a Docker image, deploy it to Docker Desktop, push it to a local Docker registry, and finally deploy it to your Kubernetes cluster.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is not licensed.
