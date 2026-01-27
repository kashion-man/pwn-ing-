FROM ubuntu:19.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y xinetd

RUN useradd -m ctf
WORKDIR /home/ctf

COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./flag /home/ctf
COPY ./flag /
COPY ./tcache_corruption_challenge /home/ctf
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

    
CMD exec /bin/bash -c "/etc/init.d/xinetd start; trap : TERM INT; sleep infinity & wait"

EXPOSE 10001