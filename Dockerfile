# Use the official Python image as the base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy your app's requirements.txt file into the container
COPY requirements.txt .

# Install the app's Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Certbot and other necessary tools
# RUN apt-get update && \
#    apt-get install -y certbot curl cron && \
#    rm -rf /var/lib/apt/lists/*

# Copy your app's source code into the container
COPY . .

# Expose the HTTPS port
EXPOSE 443

# Set the entrypoint script as the default command
CMD ["python", "main.py"]
