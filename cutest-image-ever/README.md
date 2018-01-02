# Part 1: the cutest image ever

## 1. Vanilla work
We are going to create our image from scratch.  
First we need an OS, i.e. wee ned the image of OS to build our application on.    
Let's get a _Debian Stretch_:  
`docker pull debian:stretch`  

It is possible to view all available image on our machine via:  
`docker images`

Now we've got the OS image, let's launch a container of this image.  
A container can be considered as an instance of an image.  
Let's start working on it:  
`docker run --tty --interactive debian:stretch`  
`--tty` opens a pseudo-term on the container, allowing us to launch command inside it.  
`--interactive` allows us to see resutls of command in std-in.  
With the short args, the command is:  
`docker run -ti debian:stretch`  

Now, we're inside the container and are able to develop our application:  
Update the package list:  
`apt-get update`  
Install _cowsay_:  
`apt-get install cowsay`  
  
**Note:** Docker always open session as _root_.    
  
Let's test it:   
`./usr/games/cowsay "hello, this is cow!"`  
Wonderful!  

Now we can leave the container:  
`exit`  
  
Back to our real terminal, let's view our container:  
`docker ps -l`  
`-l` stands for `--latest` which show only the latest container.  
You can see that our container has a strange/funny name. It is randomly picked by Docker.  

It's now time to create our image! For this we'll use:  
`docker commit -m "_my-message_" _my-container-name_ _wanted-image-name_:_wanted-image-tag_`   
  
`docker commit -m "My first image, yeah!" vigilant_snyder cutest-image-ever:v0
`  

Now when listing images, we can see our image:  
`docker images`  

Let's test it:  
`docker run --rm cutest-image-ever:v0 ./usr/games/cowsay "Am I working?"`  
`--rm` is for automatically removing container after use  

Check if `rm` is really working:
`docker ps -a`  
`-a` stands for `--all`  

Hooray, you've made your first image.  
  
Seems like our cow has something to say:  
`docker run --rm cutest-image-ever:v0 ./usr/games/cowthink "Is it really a good idea to create image from container?"`  
No, because:
  -  it will produce heavier images (even if we can't see it with our example)
  -  you have to share the entire image
  -  there is no way to tweak it

## 2. Meet Dockerfile
The right way to define an image is to write a Dockerfile.  
See Dockerfile.x for comments.  

Now that we have a Dockerfile, we can build an image from it:
`docker build --tag cutest-image-ever:v1 .` 

View our new image:  
`docker images`  

And use it:  
`docker run --rm cutest-image-ever:v1`  
  
Even if CMD is set, it is still possible to override it:  
`docker run --rm cutest-image-ever:v1 ./usr/games/cowsay -e "O-" -T " U"  "I can override myself!"`  

## 3. Add your first config
Seems like our cow has something to say again:  
`docker run --rm cutest-image-ever:v1 ./usr/games/cowthink "./usr/games/cowsay is too long to write!"`  

Let's try to do it the wrong way first, just to figure what is required.  
First, connect to a container via bash:  
`docker run --name config_path -ti cutest-image-ever:v1 bash`  
Here we give the container a name in order to idenitfy oit quickly in the list.  

Inside the container, configure the path:  
`export PATH=$PATH:/usr/games`  
Test it:  
`cowsay "Wonderfully easy"`  
And exit the container:  
`exit`  
  
Let's display our container info:  
`docker ps -l`  
We can see that our continer is correctly named 'config_path'.  

Now, we could _commit_ our changes to a new image but we learn that it's not a good practice. Let's update our Dockerfile instead.  

Build the new image:  
`docker build --tag cutest-image-ever:v2 .`  
See the "Using cache" message?  
It indicates that if the layer has been previously executed, it won't be executed again but retrieved from cache instead. Layers are shared between all images!

Test it:  
```
docker run --rm cutest-image-ever:v2
docker run --rm cutest-image-ever:v2 cowsay "Wow, so easy!"
```

## 4. To the cutest and beyond
Seems like our cow has something to say again:  
```
docker run --rm cutest-image-ever:v2 cowthink "Who am I?"
docker run --rm cutest-image-ever:v2 cowsay -f vader "I am your father"
docker run --rm cutest-image-ever:v2 cowsay -f unipony "F*** startups, I want to be a cat!"
```

Ok, let's see if our cow can be a cat:  
`docker run --rm cutest-image-ever:v2 cowsay -l`  
Hummm, that's not the case...

Let's figure out how to do it!  
First, connect into a temporary container (we only need it for tests, it will be useless after that):  
`docker run --rm -ti cutest-image-ever:v2 bash`

Inside the container, open and edit a _cat.cow_ file:
```
vi /usr/share/cowsay/cows/cat.cow
nano /usr/share/cowsay/cows/cat.cow
```
Doesn't work. It's normal: our base image is a bare debian!  
Let's install vim then:  
`apt-get install vim`  
And now, edit our file:  
`vim /usr/share/cowsay/cows/cat.cow`  
And test if we did well:  
`cowsay -f cat "Oh, so cute!"`  

Now that we figured out what to do, let's edit our Dockerfile.  
Build our new image:  
`docker build --tag cutest-image-ever:v3 .`

And test it:  
`docker run --rm cutest-image-ever:v3`  

And that's it, the cutest image ever!  

## 5. Publish and share
Now, we want to share our cute image with the rest of the world.  

### 5.1. Give the image a proper name
So far we give the name we want to our image. But if we want to publish, it must respect a certain format:  
`_repository-name_/_image-name_:_image-tag_ ` 

To give a proper name to our image, we'll use `docker tag` which has the following syntax:   
`docker tag source_image_name:souce_image_tag target_image_name:target_image_tag`

### 5.2. Publish on dockerhub
First give your image a proper name:  
`docker tag cutest-image-ever:v3 dominiquev/cutest-image-ever:v3`  
Login to the registry:  
`docker login`  
And finally, send the image to the registry:  
`docker push dominiquev/cutest-image-ever:v3`

### 5.3. What happened if tag is not specified ?
Don't give a tag to our image:  
`docker tag cutest-image-ever:v3 dominiquev/cutest-image-ever`  
List images:  
`docker images`  
Image is tag with the "latest" tag. "latest" is the default tag.
**"latest" is not version. DO NOT use images with this tag, you don't know what's in them!**

##### 5.3. Publish on Gitlab
###### Connect to gitlab registry
Gitlab makes it clear:  
![Connect & use gitlab registry](https://git.kwankodev.net/dominique.vassard/docker-training/raw/part-1-cutest-image-ever/cutest-image-ever/images/gitlab_registry.png "Gitlab registry")  
Gitlab will aske for your username / password.  
###### Give the image a proper name
As gitlab advised, your image needs to have a proper name.  
Let's create ours:
`docker tag cutest-image-ever:v3 registry.kwankodev.net/dominique.vassard/docker-training/cutest-image-ever:v3.0`  
And push it:  
`docker push registry.kwankodev.net/dominique.vassard/docker-training/cutest-image-ever:v3.0`  

And that's all, everyone can now `docker pull` the image and have a cute application.