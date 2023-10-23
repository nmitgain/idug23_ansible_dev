#EDIT HERE
cp /vagrant/v11.5.8_linuxx64_server_dec.tar.gz .
docker build -t "ubuntu-db2" .
rm v11.5.8_linuxx64_server_dec.tar.gz

