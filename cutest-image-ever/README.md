_Get debian stretch image_
docker pull debian:stretch

_Launch a container and connect into it_
docker run -ti debian:stretch

_-> Inside container_
_Update repositories_
apt-get update
_Install cowsay_
apt-get install cowsay

_Test it_ 
./usr/games/cowsay "hello, this is cow!"

_List last used container_
docker ps-l
(Name is defined randmoly by docker)

_Create an image from this container_
syntax: docker commit -m "my_message" mycontainer_name wanted_image_name:wanted_image_tag
docker commit -m "My first image, yeah!" vigilant_snyder cutest-image-ever:v0

_List images_
docker images

_Test it_
docker run --rm cutest-image-ever:v0 ./usr/games/cowsay "Am I working?"
(--rm is for rautomatically removing container after use)

_List containers_
docker ps
(No new container visible)

_Now..._
docker run --rm cutest-image-ever:v0 ./usr/games/cowthink "Is it really a good idea to create image from container?"
(No, because:
  -  it will produce heavier images
  -  you have to share the entire image
  -  ther is no way to tweak it)


_Meet the docker file_
See Dockerfile for comments

_Use the image_
docker run --rm cutest-image-ever:v1

_Force a new CMD_
docker run --rm cutest-image-ever:v1 ./usr/games/cowsay -e "O-" -T " U"  "I can override myself!"

_Now..._
docker run --rm cutest-image-ever:v1 ./usr/games/cowthink "./usr/games/cowsay is too long to write!"

_One way to do it_
_Connect into new container via bash_
docker run --name config_path -ti cutest-image-ever:v1 bash
_Configure path_
export PATH=$PATH:/usr/games
_But we saw that it's not a good practice to do so_
_Let's edit Dockerfile instead_
_Build the new image_
docker build --tag cutest-image-ever:v2 .
(See the 'Usin cache' message. It indicates that if the layer has been previously executed, it won't be executed again but retrieved from cache instead. Layers are share between all images!)
_Test it_
docker run --rm cutest-image-ever:v2
docker run --rm cutest-image-ever:v2 cowsay "Wow, so easy!"

_Now..._
docker run --rm cutest-image-ever:v2 cowthink "Who am I?"
docker run --rm cutest-image-ever:v2 cowsay -f vader "I am your father"
docker run --rm cutest-image-ever:v2 cowsay -f unipony "F*** startups, I want to be a cat!"
_okay, does this exists_
docker run --rm cutest-image-ever:v2 cowsay -l

_Figure how to do it_
docker run --rm -ti cutest-image-ever:v2 bash
_-> Inside cotnainer_
vi /usr/share/cowsay/cows/cat.cow
nano /usr/share/cowsay/cows/cat.cow
(Both don't as it is a bare debian, then)
_install vim_
apt-get install vim
_Add desired file_
vim /usr/share/cowsay/cows/cat.cow
_Test_
cowsay -f cat "Oh, so cute!"

_Now in Dockerfile_
_Build it_
docker build --tag cutest-image-ever:v3 .

_Test it_
docker run --rm cutest-image-ever:v3

And that's it, the cutest image ever!

_Publish_
_Give the image a proper name_
(Image name should be repo_name/image_name:image_tag)
docker tag syntax: docker tag source_image_name:souce_image_tag target_image_name:target_image_tag
_For dockerhub_
docker tag cutest-image-ever:v3 dominiquev/cutest-image-ever:v3
_First, login to registry_
docker login
_Send image to dockerhub registry_
docker push dominiquev/cutest-image-ever:v3

_What happened if tag is not specified_
docker tag cutest-image-ever:v3 dominiquev/cutest-image-ever
docker images
(Image is tag with the "latest" tag. "latest" is the default tag.
"latest" is not version)

##### Publish on Gitlab
###### Connect to gitlab registry
Gitlab makes it clear:
![Connect & use gitlab registry](https://git.kwankodev.net/dominique.vassard/docker-training/raw/training/cutest-image-ever/images/gitlab_registry.png "Gitlab registry")
###### Give the image a proper name