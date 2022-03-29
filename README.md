# Info
This repository is a submodule that is part of my senior thesis research. You may clone this if you are only interested in the CTFs, however the full repository can be found [here](https://github.com/brendonky18/Honors-Thesis).

This *README* is meant as a guide for anyone who wants to use any of these modules on how to set up the environment to run these modules. Do not provide users with access to this file or repository as it contains write-ups for all of the solutions for each challenge. 

# CTF 1: Going Backwards
## Solution
The solution to this module can be found [here](going-backwards/writeup.md).

## Setup Instructions
### Requirements
To run this, you must have `docker`, and `docker-compose` installed. `docker-compose` must be at least version 1.28, as of this writing, 1.25 is the version installed through `apt-get docker-compose`, you can install a more recent version by using `pip install docker-compose` instead, please note that you must first uninstall any other versions you have before installing the newer version. You must also have a network called `nw0` with the subnet 172.20.30.0/24. 
You can create the network with the following command:

    docker network create nw0 --subnet 172.20.30.0/24

You may need to run it as `sudo`. Next download the [`docker-compose.yml`](going-backwards/docker-compose.yml) file. 

### **To start the server**

In the same directory as the file, run

    docker-compose up

### **To stop the server**

Also in the same directory, run

    docker-compose down -t 0

Everything else will be set up automatically.

# CTF 2: Crypto Cracking
## Solution
The solution to this module can be found [here](crypt-cracking/writeup.md).

## Setup Instruction
This has almost the same requirements and setup process. Download the [`docker-compose.yml`](going-backwards/docker-compose.yml) file. Create a network called `nw0`. Use the `docker-compose` command to start and stop the server.
Additionally, it requires a number of environment variables to be set, to do this, you must also have the [`.env`](going-backwards/.env) file downloaded in the same directory.
