 # Python implementation
 - [x] Complete client programs
   - [x] Brute forcing small primes
     - Simplest
   - [x] *e* and *m* too small for a large public key (w/o any padding)
     - Moderate
   - [x] Fermat's factorization
     - hardest (unlikely to solve on own w/o prior knowledge)
   - [ ] Refactor common code
 - [ ] Complete server programs
   - [x] Basic server implementation
     - [x] Opens and listens on port
     - [x] Successfully decodes client message
 - [ ] Complete startup client script
   - [ ] At startup, each client will send 2 numbers 
     - Random numbers? (between 2000 and 65536) or pre-determined numbers?
     - Tells the server which port to use for the next phase of the challenge
     - Same numbers will be sent as the messages as well.
     - Combine all 3 numbers to get the final flag
 - [ ] Complete startup server script

# Dockerize
 - [ ] Implement in docker
   - [ ] Create docker network
     - [ ] Create dummy containers on network
   - [ ] Create docker container running server
   - [ ] Create docker container for client
     - Brute force
     - Small *e*
     - Fermat
     - Has all needed python packages
     - Has tcpdump
   - [ ] Create docker container for student
     - Has all of the necessary tools
       - Wireshark
       - nmap
   - [ ] Create docker-compose
     - [ ] All containers are on same network
     - [ ] Set up tcp-dump w/ wireshark so student container can monitor the client container's traffic
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
