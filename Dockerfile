# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5002

# Set the environment variable for Flask
ENV FLASK_APP=realestatepriceprediction.py

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5002"]

