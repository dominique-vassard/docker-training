# Part 2: A clairvoyant application

## 0. Goal
We're going to build a very simple application that tells the future given an astrological sign.  
Application will just provides a prediction for a given astrological sign.

## 1. First version

## 2. Clairvoyant Web API
### 2.1 Configure and start the server
### 2.2. A better access to code  

## 3. What about changing python version?

## 4. Add a real database
### 4.1. Getting mysql to work
### 4.2. Use mysql from code
To connect to our database, we need its name/IP.  
So why not use the container IP?  
It can be found at the infos given by `docker inspect irma-mysql`.  

First, update the codebase in order to use database instead of CSV file.  
And build a new image as we have new dependencies.  
`docker build -t clairvoyant-app:v3-mysql .`  
  
Destrou current api container:  
`docker rm -f irma-api`  
And launch a new one:
```
docker run -d \
-p5000:5000 \
--name irma-api \
--mount type=bind,source=$(pwd),target=/home/clairvoyant-app \
clairvoyant-app:v3-mysql
```
  


Then launch database initialization:  
`docker exec -ti irma-api flask initdb`  
Tests:  
```
docker exec -ti irma-api python tests/test_irma_unit.py
docker exec -ti irma-api python tests/test_irma_integration.py
```
  
And finally, test in browser:  
`http://127.0.0.1:5000/irma/aries`  
It works!

But there is 2 problems:
- when a container is launched, we can't know for sure what will be its IP
- our db container is just a mysql without data. When relaunching, it will be a fresh database without data!  

### 4.3. The right way to connect containers  

## 5. The data problem

## 6. One application, one command
