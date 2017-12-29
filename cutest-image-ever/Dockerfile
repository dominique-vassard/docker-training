# The image from which our own image will be built on
FROM debian:stretch

# Shell commands to execute
RUN apt-get update && \
    apt-get install -y cowsay

# Specify environment variable
# ENV env_var env_value can be translated as : export env_var=env_value
ENV PATH $PATH:/usr/games

# Copy a file fro lcoal source to container target
COPY cat.cow /usr/share/cowsay/cows/

# Command to be executed a container launch
CMD ["cowsay", "-f", "cat", "Mewow, I'm so cute!"]
# This also works
# CMD cowsay -f cat "Mewow, I'm so cute!"
