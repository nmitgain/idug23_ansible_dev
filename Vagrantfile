# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  
    config.vm.box = "ubuntu/jammy64"
    config.vm.box_url = "https://app.vagrantup.com/ubuntu/boxes/jammy64"

   config.vm.network :forwarded_port, guest: 22, host: 2224, id: 'ssh'  
   config.vm.provider "virtualbox" do |vb|
		vb.gui = false
        vb.memory = "8192"
		vb.cpus = "6"
        vb.name = "ansible-dev-ubuntu-neu"
        vb.customize ['modifyvm', :id, "--hwvirtex", "on" ]
   end
  
   config.vm.provision "shell", inline: <<-SHELL
     apt update
     apt upgrade -y
	 apt dist-upgrade -y 
	 apt install docker.io ansible -y
	 apt install python3-ansible-runner python3-pandas -y  
	 apt clean
	 usermod -aG docker vagrant 
     service docker start
     docker network create ansible --subnet=172.19.0.0/16 --gateway=172.19.0.1
     docker network create db2 --subnet=172.20.0.0/16 --gateway=172.20.0.1
     docker network create hadr --subnet=172.21.0.0/16 --gateway=172.21.0.1
	 # copy over some ssh-keys so vagrant user always has the same key
	 # Also, this key is inserted in my GitLab-Profile
     cp /vagrant/ssh/id_rsa* /home/vagrant/.ssh/.
     chmod 644 /home/vagrant/.ssh/id_rsa.pub
     chmod 600 /home/vagrant/.ssh/id_rsa
     cat /home/vagrant/.ssh/id_rsa.pub >> /home/vagrant/.ssh/authorized_keys
	 chown vagrant:vagrant /home/vagrant/.ssh/*
	 # edit sshd-config to enable password auth
     sed -i -e 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config 	 
	 service ssh restart
     
   SHELL
   # Edit and uncomment according to your needs
#   config.vm.synced_folder 'G:\Downloads\itgain', "/software"
 
end
