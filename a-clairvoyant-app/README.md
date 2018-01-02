# Part 2: A claivoyant application

## Goal
We're going to build a very simple application that telles the future given an astrological sign.  
Application will just provides a prediction foir a given astrological sign.

## v0: First version
The application is as simple as it sounds.  
It accepts an argument from command line, read result from a csv fil and print result.  
Test ensures that everything works fine.

Build it:  
`docker build -t clairvoyant-app:v0 .`
  
Test application:  
```
docker run --rm clairvoyant-app:v0 python tests/test_irma_unit.py
docker run --rm clairvoyant-app:v0 python tests/test_irma_integration.py
```
  
Use the application:  
`docker run --rm clairvoyant-app:v0 python app/irma.py aries`
  

## v1: Clairvoyant Web API
### v1.0: Configure and start the server
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


### v1.1: A better access to code  
We have a workinf server, but now we need to stitch all parts together in order to our application to work. 
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

How nice is this with the automatic reload of flsk debug?  
 