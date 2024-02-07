# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 9999 available to the world outside this container
EXPOSE 22

# Run server.py when the container launches
CMD ["python", "givemethechicken.py"]
