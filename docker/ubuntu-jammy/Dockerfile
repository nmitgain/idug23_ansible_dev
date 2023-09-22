FROM ubuntu:jammy
ENV DEBIAN_FRONTEND="noninteractive"
RUN apt-get update && apt-get upgrade -y && apt-get dist-upgrade -y && apt-get install -y openssh-server mailutils
RUN mkdir /var/run/sshd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

WORKDIR /root/.ssh
COPY id_rsa.pub authorized_keys

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile
RUN chmod 600 authorized_keys
EXPOSE 22 80 3306 50000
CMD ["/usr/sbin/sshd", "-D"]
