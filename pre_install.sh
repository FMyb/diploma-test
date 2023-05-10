sudo apt update
sudo apt install gcc make libprotobuf-dev libprotobuf-c-dev protobuf-c-compiler protobuf-compiler python3-protobuf pkg-config libbsd-dev iproute2 libnftables-dev libcap-dev libnl-3-dev libnet-dev libaio-dev libgnutls28-dev python3-future git asciidoc-base xmlto
wget http://github.com/checkpoint-restore/criu/archive/v3.17.1/criu-3.17.1.tar.gz
sudo tar xzvf criu-3.17.1.tar.gz 
cd criu-3.17.1/
make clean
sudo make install
sudo criu check
sudo criu check --all
cd ..
sudo mkdir /etc/criu
sudo nano /etc/criu/runc.conf
# tcp-close
# mb file-locks

sudo apt install podman
podman -v
sudo nano /etc/containers/registries.conf
# [registries.search]
# registries=["docker.io"]

sudo podman info
sudo apt install runc
sudo nano /usr/share/containers/containers.conf 


# runtime = "runc"
# runtime_supports_json = ["crun", "runc"]
# [engine.runtimes] uncomment runc /usr/sbin/runc

sudo podman info

sudo apt install s3fs
mkdir fmyar-diploma-test
sudo nano /etc/fuse.conf 
# uncooment user_allow_other

AWSSECRETACCESSKEY=YCPHQY_dFg-K1ADSjd5uGA9u5gKTdQP9gaEzw07X AWSACCESSKEYID=YCAJExOvLBjN2HbsMqk0yQksw /usr/bin/s3fs -f -d -d fmyar-diploma-test /home/fmyar/fmyar-diploma-test -o url=https://storage.yandexcloud.net/ -o allow_other -o rw -o mp_umask=0000 -o umask=0000 -o use_cache=/tmp -o enable_noobj_cache -o kernel_cache -o max_background=1000 -o max_stat_cache_size=100000 -o multipart_size=52 -o parallel_count=30 -o multireq_max=30 -o connect_timeout=60 -o readwrite_timeout=60
