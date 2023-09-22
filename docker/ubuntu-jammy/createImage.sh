cp ~/.ssh/id_rsa.pub .
docker build -t "ubuntu-jammy" .
rm id_rsa.pub
