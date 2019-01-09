FROM ubuntu:14.04
MAINTAINER Yue Yin <yinyueacm@gmail.com>

RUN apt-get update && apt-get install -y \
    openssh-server \
    gcc \
    gcc-multilib \
    build-essential \
    libssl-dev \
    libffi-dev \
    python \
    gdb \
    vim \
    python-dev \
    python-pip
    
RUN mkdir /var/run/sshd

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22

RUN pip install pwntools
RUN pip install -U capstone
RUN pip install ropgadget

RUN useradd -m -s /bin/bash -u 8765 guest
RUN echo guest:123456 | chpasswd
RUN useradd -M -s /bin/bash -u 9876 ctf
RUN echo ctf:BigbangtheorY | chpasswd
CMD ["/usr/sbin/sshd", "-D"]
