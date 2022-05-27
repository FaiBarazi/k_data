# Pipeline Exercise
* Overview
* Repo content
* Setup
* Server calls
* Stopping the service.

## Overview:
The web service builds 2 containers; flask web application container and a mongoDB NoSQL database.

## Repo content:
* docker-compose.yml: docker instructions to handle the deployment of different containers.
* app: Flask web application.
  * Dockerfile: particular instructions for the web application container setup
  * main.py: The flask app code with the logic of handling the GET calls.
  * requirements.txt: python lib requirements to run the service.

* data: 1 csv file:
  * sample_mixed_comma.csv: the sample_mixed.csv  file with the delimiter changed
  to "," using pandas.

## Setup:
Make sure you have docker and docker-compose installed.
Clone the repo locally and cd to it.
Then follow these steps:

* Run docker compose to build all the services. the 'd' - detached - flag could be ommited:
`$ docker-compose up -d`

* Run an interactive shell using:
`$ docker exec -it mongodb bash`

* Log in to mongo DB using the root username and password defined in docker-compose.
`$ mongo -u mongodbuser -p mongodbpass`

* Create a flaskdb with use command
```> use flaskdb;`

* Create db user using the user provided in the docker-cmpose for flask
```
> db.createUser({user: 'flaskuser', pwd: 'flaskpass', roles: [{role: 'readWrite', db: 'flaskdb'}]})
> exit
```
* Log in into authenticated DB with the following, then exit db and interactive shell.
```
$ mongo -u flaskuser -p flaskpass --authenticationDatabase flaskdb;
> exit
```

* Copy the csv files to mongodb container:

```
$ docker cp data/sample_mixed_comma.csv mongodb:/tmp/vessels.csv
```

* Import the 2 json files into flaskdb as 2 collections.:
```
docker exec -i mongodb sh -c 'mongoimport -d flaskdb -c vessels -u flaskuser -p flaskpass --type=csv --headerline --file /tmp/vessels.csv --drop'
```
## Making server RESTFUL API calls:
We can use `curl`from the command line to the different endpoints. Note that the 5000 port
is mapped to port 80 on host. This can be changed as well in the docker-compose file.

* Main page call to make sure it is working:
`$ curl -i http://127.0.0.1:80`

* Get all 'dirty' vessels:
`$ curl -i http://127.0.0.1:80/dirty/vessels`

* Get all 'dirty' number of barrels with optional start_date / end_date:

```
# query params are optoinal
$ curl -i http://127.0.0.1:80/dirty/barrels?start_date=<year-month-day>&end_date=<year-month-day>
```

## Stopping the containers:
To stop the service with all the container connections run:
`$docker-compose down`

**NOTE**:
Possbily in this case, it could be best to use GraphQL to minimise the complexity of endpoints and reduce the data transfer of the queried data.

