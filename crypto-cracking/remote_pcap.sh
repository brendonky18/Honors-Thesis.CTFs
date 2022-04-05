#!/bin/bash
# USAGE:
# ./remote_pcap.sh [user_num (0, 1, 2)] [student user name]

if [[ -z ${1+x} || ( "$1" -ne 0 && "$1" -ne 1 && "$1" -ne 2 ) ]]
then
    echo "User number invalid, must be 0, 1 or 2"
elif [ -z ${2+x} ]
then
    echo "Student user name not provided"
else
    ssh -J $2@cs561.cs.umass.edu:56151 -T user$1@172.20.30.10$1 | wireshark -k -i - 
fi
