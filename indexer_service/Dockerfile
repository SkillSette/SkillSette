# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app
COPY ./requirements.txt /usr/src/app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code
COPY ./ /usr/src/app

# Make port 5000 available to the world outside this container
EXPOSE 4000

# Run main.py when the container launches
CMD ["python", "./app.py"]
