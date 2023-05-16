# Use the official Python image as the base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy app's requirements.txt file into the container
COPY requirements.txt .

# Install the app's Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install OpenSSL
RUN apt-get update && apt-get install -y openssl

# Copy your app's source code into the container
COPY . /app

# Expose a port
EXPOSE 8888

# Set the entrypoint script as the default command
CMD ["python", "main.py"]
