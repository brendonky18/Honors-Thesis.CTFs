# Guidelines for setting up your CTF for integration into CTFd

Challenges incorporated to CTFd are required to follow a stipulated directory structure and include certain necessary files. This lets the challenges get auto-registered on the platform, and also allows for better management via code. All challenges are deployed using docker containers and interact with the SSH jump server using docker networking. Following are the files that should be present in the challenge folder root:

* `meta.yml`: This file stores the name of the challenge, category, description, flag, score and hints
* `writeup.md`: The solution to the challenge goes here
* `flag.txt` [Optional]: Required if the flag is to be read as a text file
* `docker-compose.yml`: All challenges are deployed using [docker-compose](https://docs.docker.com/compose/). The command is `docker-compose up`. All the necessary services ought to start up using this single command.
* `Dockerfile` [Optional]: Optionally, you can refer to the dockerfile from the docker-compose

All containers are expected to have static IP addresses so that connection instructions provided in the challenge description are in sync with the actual setup. You can configure a static IP address for the containers in the docker-compose.yml file. All containers are expected to be connected to a preconfigured network known as nw0. Please select a random IP address from the subnet 172.20.30.0/24 for your containers. You can find the relevant section for networking in the docker-compose.yml file. You do not have to worry about conflict with others' challenges, we will resolve that from our end.
Please check the attached folder for a sample challenge ([Can You Keep Up?](https://drive.google.com/file/d/1Q1CuhcZXQsipJzKn39DZk9pLJtNfda5f/view?usp=sharing)) that has been set up following the above guidelines.
