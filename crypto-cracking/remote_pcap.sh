#!/bin/bash
# USAGE:
# ./remote_pcap.sh [user_num (0, 1, 2)] [student user name]

 ssh -J $2@cs561.cs.umass.edu:56151 user$1@172.30.20.10$1 "cat /tmp/remote_pcap" | wireshark -k -i - 
