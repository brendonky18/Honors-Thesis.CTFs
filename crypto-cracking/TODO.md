 - [x] Complete client programs
   - [x] Brute forcing small primes
     - Simplest
   - [x] *e* and *m* too small for a large public key (w/o any padding)
     - Moderate
   - [x] Fermat's factorization
     - hardest (unlikely to solve on own w/o prior knowledge)
   - [ ] Refactor common code
 - [ ] Complete server programs
   - Each client will send a random number (between 2000 and 65536), which tells the server which port to use for the next phase of the challenge
 - [ ] Implement in docker
   - [ ] Create docker network
     - [ ] Create dummy containers on network
   - [ ] Create docker container running server
   - [ ] Create docker container for each client
     - Brute force
     - Small *e*
     - Fermat
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
