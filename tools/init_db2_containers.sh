#!/bin/bash
docker run -it -d --ip 172.20.0.2 --network=db2 -p 50001:50000 --privileged --hostname=db2host1 --name=db2host1 ubuntu-db2
docker run -it -d --ip 172.20.0.3 --network=db2 -p 50002:50000 --privileged --hostname=db2host2 --name=db2host2 ubuntu-db2
docker run -it -d --ip 172.20.0.4 --network=db2 -p 50003:50000 --privileged --hostname=db2host3 --name=db2host3 ubuntu-db2
docker run -it -d --ip 172.20.0.5 --network=db2 -p 50004:50000 --privileged --hostname=db2host4 --name=db2host4 ubuntu-db2
