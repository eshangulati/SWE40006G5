# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the image
COPY requirements.txt /app

# Copy the application code into the image
COPY app.py /app

# Copy the tests into the image
COPY unittests /app/unittests
COPY seleniumtests /app/seleniumtests

# Set PYTHONPATH to make sure app.py can be found
ENV PYTHONPATH=/app

# Set the environment variable in Dockerfile
ENV PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus_multiproc_dir

# Make sure the directory exists
RUN mkdir -p /tmp/prometheus_multiproc_dir

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 80

# Command to run the Flask app
CMD ["python", "app.py"]
