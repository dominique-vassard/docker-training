# Base image for our application
FROM python:3

# Create application directory
RUN mkdir -p /home/clairvoyant-app

# Set default work directory, all commands will be launched from here
# When accessing container, we'llin this directory
WORKDIR /home/clairvoyant-app

# Copy dependencies list
COPY requirements.txt /home/clairvoyant-app

# Download and install dependencies
RUN pip install -r requirements.txt

# Copy source
COPY . /home/clairvoyant-app

# Set PYTHONPATH for test to work / Flask app
ENV PYTHONPATH=/home/clairvoyant-app FLASK_APP=/home/clairvoyant-app/app/irma_api.py FLASK_DEBUG=1

# Expose app port
EXPOSE 5000

# Run server!
CMD ["flask", "run", "--host", "0.0.0.0"]