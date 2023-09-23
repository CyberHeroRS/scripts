#!/bin/bash

set -e

j=0
cap=capture

while :
do


        sudo rsync -Pav -e "ssh -i ./ctf.pem" ./*.pcap ctf@13.81.33.90:/home/ctf/tulip/tulip/services/test_pcap
 tshark -i br-2e41af42b2d5 -i br-767059b5cc65 -i br-61f0a9730558 -i br-7680633083ab -i br-a142acb5cd25 -i br-45e6509cbfb1 -a duration:20 -w ./$cap$j.pcap          

        sudo rsync -Pav -e "ssh -i ./ctf.pem" ./*.pcap ctf@13.81.33.90:/home/ctf/tulip/tulip/services/test_pcap


        rm *.pcap

        j=$((j+1))

done

