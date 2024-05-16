# Use an official Python runtime as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app


COPY requirements.txt /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the current directory contents into the container at /app
COPY . /app

# Command to run the app using Gunicorn with Uvicorn workers
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
