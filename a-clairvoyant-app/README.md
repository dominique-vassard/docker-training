# Part 2: A clairvoyant application

## 0. Goal
We're going to build a very simple application that telles the future given an astrological sign.  
Application will just provides a prediction foir a given astrological sign.

## 1. First version

## 2. Clairvoyant Web API
### 2.1 Configure and start the server
### 2.2. A better access to code  
We have a working server, but now we need to stitch all parts together in order to our application to work. 
It can be very time-consuming to have to build our image each time we change the code....
There is a solution for this problem: we can mount our application directory on a container directory, therefore our code changes will be automatically replicated insiode the container.

First, stop our previous container:  
`docker stop irma-api`  
And delete it, because two containers cannot share the same name:  
`docker rm irma-api`  

Now we can create a container with a volume:  
```
docker run -d \
-p5000:5000 \
--name irma-api \
--mount type=bind,source=$(pwd),target=/home/clairvoyant-app \
clairvoyant-app:v1-web-api-server
```

How nice is this with the automatic reload of flask debug?  
  
Now, we still need to update our code and our tests to use our server.  

Once done, build a new image (because we have new dependencies):  
`docker build -t clairvoyant-app:v1-1-web-api-mount .`  
  
And launch a new container:  
```
docker run -d \
-p5000:5000 \
--name irma-api \
--mount type=bind,source=$(pwd),target=/home/clairvoyant-app \
clairvoyant-app:v1-1-web-api-mount
```

To launch tests, you could connect into the container via:  
`docker exec -ti irma-api bash`  
And launch your tests from here.  
  
But it's not a goo practice. In theory, you should never work from inside your container.  
How do I laucnh my tests then?  
Remember how you lauch command on your cutest image?  
The same applies for running container, even if syntax if slightly different:  
`docker exec -ti _your_command_`  
For our tests, it will be:  
```
docker exec -ti irma-api python tests/test_irma_unit.py
docker exec -ti irma-api python tests/test_irma_integration.py
```

You can now test our mighty api: 127.0.0.1:5000  

## 3. What about changing python version?

## 4. Add a real database
### 4.1. Getting mysql to work
### 4.2. Use mysql from code
### 4.3. The right way to connect containers  

## 5. The data problem

## 6. One application, one command