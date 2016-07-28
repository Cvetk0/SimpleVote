FROM alpine

# Add python to image
RUN apk add --no-cache python

# Get pip installer and install pip
COPY get-pip.py /tmp/
RUN python /tmp/get-pip.py

# Install python flask and redis libraries
RUN pip install flask redis

# Add the application
ADD app /app

# Set run command to start the application
CMD ["/usr/bin/python", "/app/run.py"]

EXPOSE 5000