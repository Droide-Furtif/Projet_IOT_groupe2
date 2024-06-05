FROM python:alpine3.11

# Copy the content of the project directory to the working directory

# Set the working directory in the container
WORKDIR /usr/src/app
COPY . . 

# Set the directive to specify the executable that will run when the container is initiated
RUN pip install -r requirements.txt

# Specify the command to run on container start
CMD [ "python" , "api.py" ]
