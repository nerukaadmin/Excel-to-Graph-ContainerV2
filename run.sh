#!/bin/sh
echo Pass argumrnt for script....
echo For all "a"
echo For team "t"
echo For role "r"
read input </dev/tty
if [ "$input" = "a" ]; then
   docker run \
   -v $(pwd)/IN:/excel/IN \
   -v $(pwd)/OUT:/excel/OUT \
   -v $(pwd)/tmp:/excel/tmp \
   -v $(pwd)/TM:/excel/TM \
   ex_to_graph:v3
   
elif [ "$input" = "t" ];then
   docker run \
   -v $(pwd)/IN:/excel/IN \
   -v $(pwd)/OUT:/excel/OUT \
   -v $(pwd)/tmp:/excel/tmp \
   -v $(pwd)/TM:/excel/TM \
   -v $(pwd)/ROLE:/excel/ROLE \
   -v $(pwd)/ROLE_TXT:/excel/ROLE_TXT \
   ex_to_graph:v3 -e t
   
else
    docker run \
   -v $(pwd)/IN:/excel/IN \
   -v $(pwd)/OUT:/excel/OUT \
   -v $(pwd)/tmp:/excel/tmp \
   -v $(pwd)/TM:/excel/TM \
   ex_to_graph:v3 -e r

fi
sudo chmod -R 777 OUT/
