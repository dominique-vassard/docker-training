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
Our data is stored in a CSV file, which is quit handy but does not scale very well. In addition, data changes wil laffect the repository, which is not recommended. 
So, let's use Mysql!  

### 4.1. Getting mysql to work
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
### 4.2. Use mysql from code
### 4.3. The right way to connect containers  

## 5. The data problem

## 6. One application, one command