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

# Generate RSA private key
RUN mkdir /etc/ssl/private_keys && \
    openssl genpkey -algorithm RSA -out /etc/ssl/private_keys/private_key.pem -pkeyopt rsa_keygen_bits:2048

# Set environment variable to private key path
ENV SECRET_KEY=/etc/ssl/private_keys/private_key.pem

# Copy your app's source code into the container
COPY . /app

# Expose the HTTPS port
EXPOSE 80

# Set the entrypoint script as the default command
CMD ["python", "main.py"]
