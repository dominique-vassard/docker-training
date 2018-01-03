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

## v2: What about changing python version?
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
This crash on python2 but not on python3, and wwe can see it.  
  
By the way, logs are accessible via `docker logs container_name`.  
`--tail number` allows you to see the last `number` lines of logs.  
`-f`, for `--follow` allows you to follow the logs, as `tail -f` should.

Let's pursue with a fully-typed python3 code. 