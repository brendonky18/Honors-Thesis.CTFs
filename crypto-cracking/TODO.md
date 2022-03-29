 # Python implementation
 - [x] Complete client programs
   - [x] Brute forcing small primes
     - Simplest
   - [x] *e* and *m* too small for a large public key (w/o any padding)
     - Moderate
   - [x] Fermat's factorization
     - hardest (unlikely to solve on own w/o prior knowledge)
   - [x] Refactor common code
   - [x] Change server and client programs to objects
 - [x] Complete server programs
   - [x] Basic server implementation
     - [x] Opens and listens on port
     - [x] Successfully decodes client message
- [ ] ~~Complete startup client script~~
   - [ ] ~~At startup, each client will send 2 numbers~~
     - ~~Random numbers? (between 2000 and 65536) or pre-determined numbers?~~
     - ~~Tells the server which port to use for the next phase of the challenge~~
     - ~~Same numbers will be sent as the encrypted messages as well.~~
     - ~~Combine all 3 numbers to get the final flag~~
   - [ ] ~~Create dummy client connections~~
     - ~~Prevents challenge from being cheesed, by forcing them to solve it in the intended order~~
     - ~~Sends random data to server~~
 - [ ] Complete startup server script
   - [ ] Open dummy sockets in response to server~~
 - [x] Restructure into python package
   - [x] Clean up imports
   - [x] Combine two identical instances of `debugger.py` <sup>[1](serv/debugger.py), [2](cli/debugger.py)</sup>
# Dockerize
 - [x] Implement in docker
   - [x] Create docker network
     - [ ] ~~Create dummy containers on network~~
   - [x] Create docker container running server
   - [x] Create docker container for client
     - Brute force
     - Small *e*
     - Fermat
     - Has all needed python packages
       - [ ] Create separate .txt for requirements list
     - Has tcpdump
   - [ ] ~~Create docker container for student~~
     - ~~Has all of the necessary tools~~
       - ~~Wireshark~~
       - ~~nmap~~
   - [x] Create docker-compose
     - [x] All containers are on same network
     - [x] Set up tcp-dump w/ wireshark so student container can monitor the client container's traffic
       - [guide](https://serverfault.com/questions/362529/how-can-i-sniff-the-traffic-of-remote-machine-with-wireshark)
            
            **Server**
            ```
            mkfifo /tmp/mypcap.fifo
            tcpdump -i em0 -s 0 -U -w - > /tmp/mypcap.fifo
            nc -l 10000 < /tmp/mypcap.fifo
            ```
            **Client**
            ```
            wireshark -ki <(nc 192.168.1.1 10000)
            ```
# CTFd Deployment
- [ ] Lock down user permissions
  - Users are able to run commands over ssh, could lead to privilege escalation
  - Make the `remote_pcap` pipe read-only
  - Remote root user pass (only needed for testing because sudo was unavailable)
- [ ] Implement static flag for user 3
  - [ ] format `SDaT_Flag{...}`