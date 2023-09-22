FROM ubuntu-jammy 
WORKDIR /root
RUN mkdir db2software
WORKDIR /root/db2software
COPY v11.5.8_linuxx64_server_dec.tar.gz v11.5.8_linuxx64_server_dec.tar.gz
WORKDIR /root/db2software
RUN dpkg --add-architecture i386
RUN apt update
RUN apt install bash libnuma1 libaio1 sudo binutils less vim w3m -y
RUN tar -xzf v11.5.8_linuxx64_server_dec.tar.gz
WORKDIR /root/db2software/server_dec
RUN apt install ksh libstdc++6:i386 libpam0g:i386 -y
RUN ./db2_install -p SERVER -n -b /opt/ibm/db2/V11.5 -y
WORKDIR /root
RUN rm -rf /root/db2software
RUN groupadd -r db2inst1 && groupadd -r db2fenc1 
RUN useradd -g db2inst1 -m -s /bin/bash -c "DB2 Instanz" -r db2inst1 && useradd -g db2fenc1 -m -s /bin/bash -c "DB2 Fenced User" -r db2fenc1
RUN mkdir /home/db2inst1/.ssh && chown db2inst1:db2inst1 /home/db2inst1/.ssh && chmod 700 /home/db2inst1/.ssh
WORKDIR /etc/ld.so.conf.d/
COPY db2.conf db2.conf
RUN ldconfig >/dev/null 2>&1
WORKDIR /etc
COPY shadow shadow
EXPOSE 22 50000
