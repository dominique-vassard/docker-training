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
Two containers can communicate with each other only if they are on the same network.  

First let's see what are the currently available network:  
`docker network ls`  
You should see at least one network (the default one): bridge  
Let's see what are the containers it holds:  
`docker network inspect bridge`  
You should see your containers in the `Containers` part of the json.  
  
So, these containers are on the same network then they should be able to communicate with each others. Let's see!  
Connect into irma-api:  
`docker exec -ti irma-api bash`  
Try to ping irma-mysql via its IP:  
`ping -w2 172.17.0.3`  
It works. Great!  
Try to ping it with its name now:  
`ping -w2 irma-mysql`  
It doesn't work. Why?  
  
Ansmwer is simple: communication via container's name works only on the created network and not on the default one....  

So let's crat a network and connect our containers to it.  
First create a network:  
`docker network create --subnet 172.25.0.0/16 irmanet`  
`--subnet` allows to force our containers IPs  
  

Inspect our newly created network:  
`docker network inspect irmanet`  
We can see that no containers are on this network.  
Let's add ours:  
`docker network connect irmanet irma-api`  
`docker network connect irmanet irma-mysql`  
  
Inspect again out network:  
`docker network inspect irmanet`  
Both our containers are present.  
  
Now, let's connect into irma-api:  
`docker exec -ti irma-api bash`  
and try to ping irma-mysql by its IP:  
`ping -w2 172.17.0.3`
and by its name:  
`ping -w2 irma-mysql`  
It works!  
  
We can now replace our hard-coded IP:
`app.config["DB_HOST"] = "172.17.0.3"`  
by the container name:  
`app.config["DB_HOST"] = "irma-mysql"`

Let's run our tests to make sure that everything works fine:  
```
docker exec -ti irma-api python tests/test_irma_unit.py
docker exec -ti irma-api python tests/test_irma_integration.py
```

While it is possible to connect containers after their creations, it is better to connect them to a network at creation. Let's do it.  
First, destroy them all:  
`docker rm -f irma-api irma-mysql`  

Then re-create api:
```
docker run -d \
-p5000:5000 \
--name irma-api \
--network irmanet \
--mount type=bind,source=$(pwd),target=/home/clairvoyant-app \
clairvoyant-app:v3-mysql
```
 
And the mysql database:  
```
docker run -d --name irma-mysql \
--network irmanet \
-e MYSQL_ROOT_PASSWORD=mysql \
-e MYSQL_DATABASE=irma \
-e MYSQL_USER=irma \
-e MYSQL_PASSWORD=cr1StalB4ll \
-p 3366:3306 \
mysql:5.7 \
--bind-address=0.0.0.0
```
  
We can inspect `irmanet` network to ensure that our containers are there:  
`docker network inspect irmanet`  
Everythinh seems fine.  
Let's launch our tests:  
`docker exec -ti irma-api python tests/test_irma_unit.py`  
Wow, every single test fails!  
What happened?  
  
It happens that when a container is created, it is following its image, and the mysql image doesn't include any data. Let's tackel this problem.  

## 5. The data problem

## 6. One application, one command