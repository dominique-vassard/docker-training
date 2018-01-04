# Part 2: A clairvoyant application

## 0. Goal
We're going to build a very simple application that telles the future given an astrological sign.  
Application will just provides a prediction foir a given astrological sign.

## 1. First version

## 2. Clairvoyant Web API
### 2.1 Configure and start the server
Having just a command line tool is sad, let's make it a Web API.  
For that, we'll need [Flask](http://flask.pocoo.org/).  

For a minimal working api, we have to:  
- add a `requirements.txt` to manage dependencies  
- install those dependencies  
- write our `irma-api.py` which will receive and treat request  
- start the server!  

Let's add needed and update our Dockerfile.  
  
Now build our image:  
`docker build -t clairvoyant-app:v1-web-api-server .`

And run it:  
`docker run --detach --port 5000:5000  --name irma-api clairvoyant-app:v1-web-api-server`  
`--detach`  or `-d` allows our container to run in background.  
`--port` or `-p` allows to map container ports.  


Container runs as long their CMD lasts. Then for a webserver, or any other background task, container will ruyn until we stop it or the process crashes.  
If we ran the container without `-d`, we'll have access to command line inside the container, but as soon as we leave it, the container dies. 


Now, if we list running containers, we can it:  
`docker ps`  


### 2.2. A better access to code  

## 3. What about changing python version?

## 4. Add a real database
### 4.1. Getting mysql to work
### 4.2. Use mysql from code
### 4.3. The right way to connect containers  

## 5. The data problem

## 6. One application, one command