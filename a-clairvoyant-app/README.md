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

## 6. Complete application in one command?
Wouldn't be nice to have our application up with just one command?  
Well, that the purpose of Docker compose.  
To install it, [follow the instructions](https://docs.docker.com/compose/install/)  
Additionally, install the (very useful) bash completions: [instructions here](https://docs.docker.com/compose/completion/)  

First, let's create our `docker-compose.yml`.  
Now that you understand how containers work, reading it should be very easy.  

Let's up our project:  
`docker-compose up -d`  
You can view what's been upped with:  
`docker-compose ps`  
  

We can run command inside docker-compose containers like this:
`docker-compose run irma-api flask initdb`  
(We don't need it as we mount a data volume)  

Let's test:  
```
docker-compose run irma-api python tests/test_irma_unit.py
docker-compose run irma-api python tests/test_irma_integration.py
```

In fact, there is nothing new as classic containers have been created, see:  
`docker ps`  
Then you can interact as before with your containers.  
  
What about network?  
Let's list them:  
`docker network ls`  
As we can see, docker-compose created its own network and put all containers he has created in it.  
Just as we did by hand.  

