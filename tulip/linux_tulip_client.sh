#!/bin/bash

set -e

aa-complain `which tcpdump`
sudo tcpdump -Z root -U -G 60 -w ./file-%H-%M-%S.pcap -z ./send_pcap.sh
