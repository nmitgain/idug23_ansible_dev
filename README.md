# idug23_ansible_dev
Vagrant, Docker, Ansible-Examples for Session F15 at IDUG 2023 EMEA

# Usage
You don't have to use all components. If you like running your own VM or on real hardware, choose the parts you need. 
## Vagrant VM
* Edit Vagrantfile to your needs. Then start the vm with
```bash
vagrant up
```
* Stop or hibernate current vm
```bash
vagrant halt
vagrant suspend
```
* Completely remove the current vm
```bash
vagrant destroy
```
## Docker Images
* ssh to the VM (user: vagrant pw: vagrant)
* create a working directory and copy the contents from the git-repository there (or checkout the repo again)
```bash
mkdir idug_workdir
cd idug_workdir
cp -r /vagrant/idug23_ansible_dev/* .
```
* Build the ubuntu-jammy-Image (edit Dockerfile if needed)
```bash
cd docker/ubuntu-jammy
./createImage.sh
```
* Build the ubuntu-db2-Image
    * Copy a Db2 installation image for linux to the Windows-Directory, where your Vagrantfile sits. The file should be seen in the /vagrant-Directory on your Linux vm.
    * Edit the Dockerfile to match the filename of your installation image
    * Edit the createImage.sh - File to match the filename of your installation image
    * Create Docker-Image (this takes a while)
    ```bash
    ./createImage.sh
    ```

## Start and initialize containers
* cd to the tools-Directory
```bash
cd ../../tools
```
* run init_db2_containers.sh
```bash
./init_db2_containers.sh
```
* run init_knownhosts.sh
```bash
./init_knownhosts.sh db2hosts.txt
```
The key-error during the live demo at IDUG Prague was simply caused by existing keys from a previous installation in the file /home/vagrant/.ssh/known_hosts. Now, this keys are removed first. If you still get this error, mmove he known_hosts-file away and run the script again.

The script init_knownhosts.sh is only needed if you had changes done to your Docker-image.The RSA-Signature of the containers will not change, even if you destroy (remove) the containers as long as you use the same docker image or the next start.  
* Test ssh-connection for the first container
```bash
ssh -l root 172.20.0.2
```
## Ansible
* cd to the ansible directory
```cd ../ansible```
* Run the 03_db2_instance_and_sample.yml playbook to create the db2inst1 instance and the Sample-Database on all targets
```bash
ansible-playbook 03_db2_instance_and_sample.yml -i inventory/ -l db2server
```

## Remarks
* you can always start/stop/remove containers with the Docker-Plugin from VSC
* when you start new containers, you don't need to initialize known_hosts again, unless the Docker-Image has changed its signature
* HAVE FUN!