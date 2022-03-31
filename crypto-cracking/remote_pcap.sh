#!/bin/bash
# USAGE:
# ./remote_pcap.sh [user_num (0, 1, 2)] [student user name]

 ssh -J -T $2@cs561.cs.umass.edu:56151 user$1@172.20.30.10$1 | wireshark -k -i - 
