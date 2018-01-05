# Docker cheatsheet

## Image
`docker pull image_name:image_tag`: Download image  
`docker images`: List images  
`docker rmi image_name:image_name`: Remove image   
`docker build -t image_name_image:tag .`: Build image based on the Dockerfile in the current directory  
`docker build --no-cache -t image_name_image:tag .`: Same as  above. Force execution of all layers wether they are cached or not.  

## Container
### General
`docker ps`: List containers  
`docker rm container_name`: Remove stopped container  
`docker rm -f container_name`: Remove running container  

### Run
Minimal command:  
`docker run image_name:image_tag`: Create a container based on given image  
###### Common options
`-t`, `--tty`: Launch a pseudo terminal inside the container  
`-i`, `--interactive`: Allows interactive control (i.e. see results of shell commands)   
`--name container_name`: Set the container name  
`--mount options`: Mount a volume on container. Options can be:  
    - `type=mount_type`: to specify the colume type (bind, volume or tmpfs)  
    - `source=mount_source`: the  mount source (a local directory or a data container)  
    - `destination=mount_destination`: the directory to mount on container  
`--network network_name`: The network to create container on  
`-p local_part:container_port`, `--publish`: Defines the port mapping  
`-e ENV_VAR=ENV_VALUE`, `--env`: Specify an ENV_VAR environment variable with an ENV_VALUE value   

###### Common usages
`docker run -ti --rm image_name:image_tag`: Create a container based on given image and start a session in it. It will be deleted when left  
`docker run -d --name container_name image_name:image_tag`: Create a container with the given name based on the given image. It will run in the background  
`docker run -d --network network_name  --name container_name image_name:image_tag`: Same as above. Will be created on the given network  
`docker run -d --mount type=bind,source=local_dir,target=container_dir --name container_name image_name:image_tag`: Create a container that runs in the background with the given name based on the given image. The local_dir will be mount as container_dir  

### Other useful commands
`docker exec -ti container_name command`: Execute `command` in the given container  
`docker exec -ti container_name bash`: Connect to the given container and provides cli  
`docker inspect container_name`: view given container's details  

## Network
`docker network ls`: List networks  
`docker network inspect network_name`: view given network  
`docker network create --subnet network_segment  network_name`: Create a network with the given name for the ip concerned by the given network_segment  
`docker network connect network_name container_name`: Connect given container on the given network  

## Compose
`docker-compose up -d`: Create and start all containers defined in the compose file  
`docker-compose down`: Stop and remove all containers defined in the compose file  
`docker-compose ps`: List containers managed by docker-compose  