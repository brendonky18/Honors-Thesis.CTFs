#!/bin/bash
# USAGE:
# ./remote_pcap.sh [user_num (0, 1, 2)] [ip address]

 ssh -p 222$1 user$1@$2 "cat /tmp/remote_pcap" | wireshark -k -i - 