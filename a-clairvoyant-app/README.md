# Part 2: A clairvoyant application

## 0. Goal
We're going to build a very simple application that telles the future given an astrological sign.  
Application will just provides a prediction foir a given astrological sign.

## 1. First version

## 2. Clairvoyant Web API
### 2.1 Configure and start the server
### 2.2. A better access to code  

## 3. What about changing python version?
That's easy as just changing the version in the Docker file! 
  
Build:  
`docker build -t clairvoyant-app:v2-python3 .`  
And launch a new container:  
```
docker run -d \
-p5000:5000 \
--name irma-api \
--mount type=bind,source=$(pwd),target=/home/clairvoyant-app \
clairvoyant-app:v2-python3
```

Test just to be sure:  
```
docker exec -ti irma-api python tests/test_irma_unit.py
docker exec -ti irma-api python tests/test_irma_integration.py
```
... and that's fail.  

Nevermind, just update the code, and now all is OK.  

Now, se have our application available both in python 2 and in python 3.  
And what's beyond marvelous, is that we can run both of same at the same time!  
Let's re-launch th python 2 but with a different port mapping.
```
docker run -d \
-p5005:5000 \
--name irma-api-p2 \
--mount type=bind,source=$(pwd),target=/home/clairvoyant-app \
clairvoyant-app:v1-1-web-api-mount
```

Got to your browser and open: `http://127.0.0.1:5005/irma/aries`  
It works!  
Now we know that our code is compatible with python 2 AND python 3.  
With our containers sharing the same code, we can code with confidence and be aware of any incompatibility that might happened.  
For example:  
We decide to type our code, then we replace:
`def read_future(sign):`  
with  
`def read_future(sign:str):`  
This crash on python2 but not on python3, and we can see it.  
  
Let's pursue with a fully-typed python3 code.  


## 4. Add a real database
### 4.1. Getting mysql to work
### 4.2. Use mysql from code
### 4.3. The right way to connect containers  

## 5. The data problem

## 6. One application, one command