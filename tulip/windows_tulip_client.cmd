 @echo off
set TULIP_IP=tulip.northeurope.cloudapp.azure.com
:loop
set FILE_NAME="file-%TIME:~0,2%-%TIME:~3,2%-%TIME:~6,2%.pcap"
tshark -i 8 -a duration:60 -w %FILE_NAME% "not udp and not icmp"
pscp-i .\scc-tulip_key.pem %FILE_NAME% scc-user@%TULIP_IP%:/home/scc-user/tulip/services/test_pcap/
goto loop
