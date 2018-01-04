# Part 2: A clairvoyant application

## 0. Goal
We're going to build a very simple application that telles the future given an astrological sign.  
Application will just provides a prediction foir a given astrological sign.

## 1. First version

## 2. Clairvoyant Web API
### 2.1 Configure and start the server
### 2.2. A better access to code  

## 3. What about changing python version?

## 4. Add a real database
### 4.1. Getting mysql to work
### 4.2. Use mysql from code
### 4.3. The right way to connect containers  

## 5. The data problem
Solve this problem is pretty simple as we've done something similar before.  
A while ago, we wanted to be able to update our code without rebuilding a new image and we mount a volume on the api container. You can view this from another point and say that we persists our changes, no matter iof there is an api container or not. The same applies for database, and solution is the same: we create a volume to store our data.  
  
First create a directory to store our data on our machine:  
`mkdir ../data`  
Destroy current mysql container:  
`docker rm -f irma-mysql`  
And re-create it with a volume:  
```
docker run -d --name irma-mysql \
--network irmanet \
--mount type=bind,source=$(pwd)/../data,target=/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=mysql \
-e MYSQL_DATABASE=irma \
-e MYSQL_USER=irma \
-e MYSQL_PASSWORD=cr1StalB4ll \
-p 3366:3306 \
mysql:5.7 \
--bind-address=0.0.0.0
```
There can be a delay before database is really up.  
  
Populate our database:  
`docker exec -ti irma-api flask initdb`  
Launch the tests:  
```
docker exec -ti irma-api python tests/test_irma_unit.py
docker exec -ti irma-api python tests/test_irma_integration.py
```
All is fine.


Now is the fun part. Destroy your container:  
`docker rm -f irma-mysql`  

And re-create it
Be aware that now your database and password are already created, then to create a new container, all is required is this:
```
docker run -d --name irma-mysql \
--network irmanet \
--mount type=bind,source=$(pwd)/../data,target=/var/lib/mysql \
-p 3366:3306 \
mysql:5.7
```
  
Launch to ensure that everything's fine:  
```
docker exec -ti irma-api python tests/test_irma_unit.py
docker exec -ti irma-api python tests/test_irma_integration.py
```
Nice, isn't it?  

## 6. One application, one command

