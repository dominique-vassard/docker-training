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
  
Let's pursue with a fully-typed python3 code. 

## v3: Add a real database
Our data is stored in a CSV file, which is quit handy but does not scale very well. In addition, data changes wil laffect the repository, which is not recommended. 
So, let's use Mysql!

### Getting mysql to work
First, pull the image:  
`docker pull mysql:5.7`  
Launch a container with a root_password:  
```
docker run -d --name container_name \
-e MYSQL_ROOT_PASSWORD=mysql_root_pass \
mysql:5.5
```

In order to make mysql accesible from anywhere add options `--bind-address=0.0.0.0`

In addition, it is possible to create database and user at container creation with the environment variable:
- `MYSQL_DATABASE=database_name`: to create a database 
- `MYSQL_USER=user_name`: to create a user (non root)
- `MYSQL_USER`: to create non root user's password

Full example:  
```
docker run -d --name irma-mysql \
-e MYSQL_ROOT_PASSWORD=mysql \
-e MYSQL_DATABASE=irma \
-e MYSQL_USER=irma \
-e MYSQL_PASSWORD=cr1StalB4ll \
-p 3306:3306 \
mysql:5.7 \
--bind-address=0.0.0.0
```

`-e` stands for `--env`, it allows to set environment variable.  
If you already have a `mysql` process running on your machine, you will encoutered the following error:  
`address already in use.`  
This means the port you try to use is not available.  
Then, just change it, it's easy!  
```
docker run -d --name irma-mysql \
-e MYSQL_ROOT_PASSWORD=mysql \
-e MYSQL_DATABASE=irma \
-e MYSQL_USER=irma \
-e MYSQL_PASSWORD=cr1StalB4ll \
-p 3366:3306 \
mysql:5.7 \
--bind-address=0.0.0.0
```
Now, mysql is on port 3366.  
  

You cann access your mysql with this (somehow barbaric) command:  
```
docker run -ti \
--link irma-mysql:mysql --rm \
mysql:5.5 sh -c 'exec mysql \
-h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" \
-uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD"'
```

To connect to mysql, we need mysql. Sounds like a circular dependency doomed to failure as we don't have mysql on our machine.  
To avoisd this problem, we will create a container from mysql image, link (more on this later) it to our working mysql and execute a command inside that last container.   
  
We can see that our database is here:  
`SHOW DATABASES;`  
And our user too:  
`SELECT User, Host, authentication_string FROM mysql.user;`

Now let's get our hands on code!  

## Use mysql from code
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
--mount type=bind,source=$(pwd),target=c \
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

## The right way to connect containers
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
First, desctroy them all:  
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

## The data problem
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

## Complete applications in one build?
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

