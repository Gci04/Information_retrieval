FROM python:3

# Create app directory
WORKDIR /application

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY . /application

WORKDIR /application/app

EXPOSE 9999
CMD [ "python", "main.py" ]
# CMD [ "python", "/application/model/api_get.py" ]

# docker build
# docker build -t "<app name>" .

# docker run
# docker run random_app -p 9999 # to make the port externally avaiable for browsers

# show all running containers
# docker ps

# Kill and remove running container
# docker rm <containerid> -f

# open bash in a running docker container
# docker exec -ti <containerid> bash

# docker compose
# run and interact between multiple docker containers

# remove any stopped containers and all unused images
# docker system prune -a
