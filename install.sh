#!/bin/sh
echo Checking Docker..
if docker --version ; then 
	echo Docker installed..
	curl https://raw.githubusercontent.com/nerukaadmin/Excel-to-Graph-Container/main/requirements.txt --output requirements.txt
	echo requirements.txt Pulled.
	curl https://raw.githubusercontent.com/nerukaadmin/Excel-to-Graph-Container/main/ex_to_graph.py --output ex_to_graph.py
	echo ex_to_graph.py Pulled.
	curl https://raw.githubusercontent.com/nerukaadmin/Excel-to-Graph-Container/main/Dockerfile --output Dockerfile
	echo Dockerfile Pulled.
	curl https://raw.githubusercontent.com/nerukaadmin/Excel-to-Graph-Container/main/init --output init
	echo init Pulled.
	echo Cretaing DIR structure..!
	mkdir -p OUT
	mkdir -p IN
	mkdir -p tmp
	mkdir -p TM
	mkdir -p ROLE
	mkdir -p ROLE_TXT
	chmod -R 777 OUT
	chmod -R 777 IN
	chmod -R 777 tmp
	chmod -R 777 TM
	chmod -R 777 ROLE
	chmod -R 777 ROLE_TXT
	touch ./TM/team_member_list.txt
	chmod 777 ./TM/team_member_list.txt
	echo Installtion completed...!
	echo Docker Image build.
	docker build -t ex_to_graph:v3 .
	echo creating run.sh
	cat init > run.sh
	rm init 
else
	echo install Docker..
	echo please visit https://docs.docker.com/engine/install/ubuntu/
fi
