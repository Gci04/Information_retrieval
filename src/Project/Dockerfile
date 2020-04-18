FROM python:3.6

# Create app directory
WORKDIR /application

# Install app dependencies
COPY model/requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY . /application

EXPOSE 8080
CMD [ "python", "/application/app/main.py" ]
