# install docker

sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt install docker-ce
sudo systemctl status docker

sudo nano /etc/docker/daemon.json

# {
#   "experimental": true
# } > /etc/docker/daemon.json

sudo systemctl daemon-reload
sudo systemctl restart docker


# install criu

sudo apt install gcc make libprotobuf-dev libprotobuf-c-dev protobuf-c-compiler protobuf-compiler python3-protobuf pkg-config libbsd-dev iproute2 libnftables-dev libcap-dev libnl-3-dev libnet-dev libaio-dev libgnutls28-dev python3-future git asciidoc-base xmlto

wget http://github.com/checkpoint-restore/criu/archive/v3.17.1/criu-3.17.1.tar.gz
sudo tar xzvf criu-3.17.1.tar.gz 
cd criu-3.17.1/

make clean
# make
sudo make install

sudo criu check
sudo criu check --all

# sudo mkdir /etc/criu
# echo tcp-close >> /etc/criu/runc.conf # sudo nano /etc/criu/runc.conf
# https://github.com/checkpoint-restore/criu/issues/2043

cd ..

# docker jupyter

sudo docker run  --name jupyter -p 8888:8888  jupyter/scipy-notebook

sudo docker checkpoint create --leave-running=true --checkpoint-dir /home/fmyar/checkpoint jupyter save16

sudo  cp -r checkpoint/save16 fmyar-diploma-test


# s3
sudo apt install s3fs
mkdir fmyar-diploma-test
sudo nano /etc/fuse.conf 
# uncooment user_allow_other
AWSSECRETACCESSKEY=YCPqApy9u-84c4SvXfjvMZ1SSsCK2Q37HFzMDW9K AWSACCESSKEYID=YCAJE_v1vflwAgAfdc75dZF1k /usr/bin/s3fs -f -d -d fmyar-diploma-test ~/fmyar-diploma-test -o url=https://storage.yandexcloud.net/ -o allow_other -o rw -o mp_umask=0000 -o umask=0000 -o use_cache=/tmp -o enable_noobj_cache -o kernel_cache -o max_background=1000 -o max_stat_cache_size=100000 -o multipart_size=52 -o parallel_count=30 -o multireq_max=30 -o connect_timeout=60 -o readwrite_timeout=60

# restore

docker create --name jupyter jupyter/scipy-notebook
 cp -r /home/fmyar/fmyar-diploma-test/save/ /var/lib/docker/containers/f4c00f6115a355219145eb31c7ed644f088afc8fcecf3776cabf99435052f4dc/checkpoints/
docker start --checkpoint save jupyter




# with podman

# install podman

sudo apt install podman
podman -v

sudo nano /etc/containers/registries.conf

# [registries.search]
# registries=["docker.io"]

podman info

# set runc in runtime

sudo apt install runc

sudo nano /usr/share/containers/containers.conf 
sudo nano /etc/containers/libpod.conf 

# runtime = "runc"
# runtime_supports_json = ["crun", "runc"]
# [engine.runtimes] uncomment runc /usr/sbin/runc

# podman jupyter

sudo podman run --name jupyter -p 8888:8888  jupyter/scipy-notebook

sudo podman container checkpoint jupyter -e /home/fmyar/save1.tar.gz --leave-running=true
# runtime runc

# restore podman

sudo podman pull jupyter/scipy-notebook
sudo podman container restore --import /home/fmyar/save1.tar.gz --name jupyter --log-level=debug



# volume
sudo docker run --user root -v /home/fmyar/jovyan:/home/jovyan/ -e CHOWN_HOME=yes -e CHOWN_HOME_OPTS='-R'  --name jupyter -p 8888:8888  jupyter/scipy-notebook start-notebook.sh --NotebookNotary.db_file=:memory:
# issue about volume to home

NotebookNotary.db_file


# sudo docker run --user root -v /home/jovyan:/home/jovyan/ -e GRANT_SUDO=yes --tmpfs /tmp --name jupyter -p 8888:8888 jupyter/datascience-notebook

# docker create --user root -v /home/fmyar/jovyan:/home/jovyan/ -e CHOWN_HOME=yes -e CHOWN_HOME_OPTS='-R' --name jupyter -p 8888:8888 jupyter/scipy-notebook



/run/containerd/io.containerd.runtime.v2.task/moby/5c8ad908076dc43ded1aab93d67e26389dfcd1010bb3f433808d65d6b72b921e/criu-dump.log

sudo docker checkpoint create --checkpoint-dir /home/fmyar/checkpoint jupyter save

docker run  --user root -v /home/yarusha/jovyan:/home/jovyan/ -e CHOWN_HOME=yes -e CHOWN_HOME_OPTS='-R' --name jupyter -p 8888:8888 jupyter/scipy-notebook /bin/true

sudo tar -czvf save.tar.gz checkpoint/save
sudo tar -czvf jovyan.tar.gz jovyan

cp save.tar.gz fmyar-diploma-test
cp jovyan.tar.gz fmyar-diploma-test


cp fmyar-diploma-test/jovyan.tar.gz .
cp fmyar-diploma-test/save.tar.gz .

sudo tar -xzvf save.tar.gz 
sudo tar -xzvf jovyan.tar.gz 



sudo docker run --user root -v ~/jovyan:/home/jovyan/ -v ~/pips:/pips -e CHOWN_HOME=yes -e CHOWN_HOME_OPTS='-R'  --name jupyter -p 8888:8888  jupyter/scipy-notebook start-notebook.sh --NotebookNotary.db_file=:memory:

sudo docker run --user root -v ~/jovyan:/home/jovyan/ -v ~/pips:/pips -e CHOWN_HOME=yes -e CHOWN_HOME_OPTS='-R' -e CHOWN_EXTRA="/pips" -e PYTHONPATH="/pips" --name jupyter -p 8888:8888  jupyter/scipy-notebook start-notebook.sh --NotebookNotary.db_file=:memory:
# https://stackoverflow.com/questions/2915471/install-a-python-package-into-a-different-directory-using-pip
nano /etc/pip.conf
[install]
target = /pips

sudo tar -czvf pips.tar.gz pips
cp pips.tar.gz fmyar-diploma-test

cp fmyar-diploma-test/pips.tar.gz .
sudo tar -xzvf pips.tar.gz


sudo swapoff -a  
free -th -s 0.5
sudo docker stats

```
tcp-close
file-locks
log-file "/home/yarusha/criu_log.log"
```


sudo docker run --user root -v ~/jovyan:/home/jovyan/ -v ~/pips:/pips -e CHOWN_HOME=yes -e CHOWN_HOME_OPTS='-R' -e CHOWN_EXTRA="/pips" -e PYTHONPATH="/pips" --name jupyter -p 8888:8888  fmyar/fmyar-diploma-jupyter start-notebook.sh --NotebookNotary.db_file=:memory:
# docker run --user root -e CHOWN_HOME=yes -e CHOWN_HOME_OPTS='-R' -e CHOWN_EXTRA="/pips" -e PYTHONPATH="/pips" --name jupyter -p 8888:8888  fmyar/fmyar-diploma-jupyter start-notebook.sh --NotebookNotary.db_file=:memory:

sudo AWSSECRETACCESSKEY=YCPHQY_dFg-K1ADSjd5uGA9u5gKTdQP9gaEzw07X AWSACCESSKEYID=YCAJExOvLBjN2HbsMqk0yQksw python3 main.py


sudo docker run --user root -v ~/jovyan:/home/jovyan/ -e CHOWN_HOME=yes -e CHOWN_HOME_OPTS='-R' --name jupyter -p 8888:8888 jupyter/scipy-notebook  start-notebook.sh --NotebookNotary.db_file=:memory:

(01.277984)    238: Error (criu/files-reg.c:2259): Can't open file opt/conda/lib/python3.10/site-packages/fasttext_pybind.cpython-310-x86_64-linux-gnu.so on restore: No such file or directory

git clone https://github.com/checkpoint-restore/criu-image-streamer.git
sudo apt install cargo
cd criu-image-streamer
make

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

aws --endpoint-url=https://storage.yandexcloud.net s3 ls --recursive s3://fmyar-diploma-test

exec 10< <(aws --endpoint-url=https://storage.yandexcloud.net s3 cp s3://fmyar-diploma-test/img-1.lz4 - | lz4 -d - -)
exec 11< <(aws --endpoint-url=https://storage.yandexcloud.net s3 cp s3://fmyar-diploma-test/img-2.lz4 - | lz4 -d - -)
exec 12< <(aws --endpoint-url=https://storage.yandexcloud.net s3 cp s3://fmyar-diploma-test/img-3.lz4 - | lz4 -d - -)

criu-image-streamer --images-dir /tmp capture | lz4 - - | aws --endpoint-url=https://storage.yandexcloud.net s3 cp - s3://fmyar-diploma-test/checkpoints/img.lz4 &
aws --endpoint-url=https://storage.yandexcloud.net s3 cp s3://fmyar-diploma-test/checkpoints/img.lz4 - | lz4 - - | criu-image-streamer --images-dir /tmp serve &