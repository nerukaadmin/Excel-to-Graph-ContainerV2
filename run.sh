#!/bin/sh
echo Pass argumrnt for script....
echo For all "al"
echo For team "tm"
echo For role "ro"
read input </dev/tty
if [ "$input" = "al" ]; then
   docker run \
   -v $(pwd)/IN:/excel/IN \
   -v $(pwd)/OUT:/excel/OUT \
   -v $(pwd)/tmp:/excel/tmp \
   -v $(pwd)/TM:/excel/TM \
   ex_to_graph:v3 al
   
elif [ "$input" = "tm" ];then
   docker run \
   -v $(pwd)/IN:/excel/IN \
   -v $(pwd)/OUT:/excel/OUT \
   -v $(pwd)/tmp:/excel/tmp \
   -v $(pwd)/TM:/excel/TM \
   ex_to_graph:v3 tm
   
else
    docker run \
   -v $(pwd)/IN:/excel/IN \
   -v $(pwd)/OUT:/excel/OUT \
   -v $(pwd)/tmp:/excel/tmp \
   -v $(pwd)/TM:/excel/TM \
   -v $(pwd)/ROLE:/excel/ROLE \
   -v $(pwd)/ROLE_TXT:/excel/ROLE_TXT \
   ex_to_graph:v3 ro

fi
sudo chmod -R 777 OUT/