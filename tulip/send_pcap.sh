#!/bin/sh

rsync -Pav -e "ssh -i ./scc-tulip_key.pem" $1 scc-user@tulip.northeurope.cloudapp.azure.com:/home/scc-user/tulip/services/test_pcap
rsync -Pav -e "ssh -i ./scc-tulip_key.pem" /var/log/suricata/eve.json scc-user@tulip.northeurope.cloudapp.azure.com:/home/scc-user/tulip/traffic

rm $1
