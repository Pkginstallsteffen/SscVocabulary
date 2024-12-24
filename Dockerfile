# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install OpenJDK 17 (Java) in the container
RUN apt-get update && apt-get install -y openjdk-17-jdk

# Set the working directory inside the container
WORKDIR /app

# Copy the local requirements.txt and your application code to the container
COPY requirements.txt /app/requirements.txt
COPY . /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the application will run on
EXPOSE 5000

# Define environment variables for your bot token and API keys
ENV BOT_TOKEN=${BOT_TOKEN}
ENV MW_API_KEY=${MW_API_KEY}
ENV THESAURUS_API_KEY=${THESAURUS_API_KEY}

# Verify Java installation
RUN java -version

# Run your Python application
CMD ["python", "main.py"]
