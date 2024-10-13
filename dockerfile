# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python dependencies (including pytest)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on (Flask uses port 5000 by default)
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]
