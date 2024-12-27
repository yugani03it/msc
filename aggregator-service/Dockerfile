# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Install any Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8085

# Define environment variables
ENV FLASK_ENV=production
ENV PORT=8085

# Run the application
CMD ["python", "app.py"]
