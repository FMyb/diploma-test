# Перенос состояния интерпретатора с помощью CRIU

## Гайд

### Подготовка системы

Весь процесс показан для Ubuntu 22.04

#### Устанавливаем criu.
```shell
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
```
проставляем конфиг
```shell
sudo mkdir /etc/criu
sudo nano /etc/criu/runc.conf
```

записываем в runc.conf

```
tcp-close
file-locks
log-file "dir to log"
```

P.S. tcp-close -- при переносе закрываем tcp соедениние, если хотим оставлять пишем tcp-established (https://criu.org/TCP_connection)

#### Устанавливаем докер

```shell
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt install docker-ce
sudo systemctl status docker
```

criu доступен только в experemental режиме докера, поэтому прописываем в конфиге

```shell
sudo nano /etc/docker/daemon.json
```
записываем
```
{
  "experimental": true
}
```
рестартем демон
```
sudo systemctl daemon-reload
sudo systemctl restart docker
```

#### Устанавливаем s3fs

Устанавливаем s3fs для переноса данных и s3 бакет

```shell
sudo apt install s3fs
```

### отключение swap'a

```
sudo swapoff -a 
```

### Перенос состояния

#### VM1

стартуем jupyter-lab образ докера, с прокинутым volume и правами root для jovyan. 

```shell
sudo docker run --user root -v ~/jovyan:/home/jovyan/ -v ~/pips:/pips -e CHOWN_HOME=yes -e CHOWN_HOME_OPTS='-R' -e CHOWN_EXTRA="/pips" -e PYTHONPATH="/pips" --name jupyter -p 8888:8888  jupyter/scipy-notebook start-notebook.sh --NotebookNotary.db_file=:memory:
```

`NotebookNotary.db_file=:memory:` -- при переносе состояния, внутренняя sqlite бд теряет права, временное решение для того чтобы пофиксить это, сделать эту бд in memory.

заходим в образ jupyter lab и в конфиг pip проставляем:

```shell
sudo docker exec -it jupyter bash
```

```shell
nano /etc/pip.conf
```

```
[install]
target = /pips
```

заходим в Jubyter lab, запускаем ячейки, сохраняем

создаем чекпоинт

```shell
sudo docker checkpoint create --checkpoint-dir ~/checkpoint jupyter save
```

архивируем чекпоинт и volume и загружаем в s3.

```shell
sudo tar -czvf save.tar.gz checkpoint/save
sudo tar -czvf jovyan.tar.gz jovyan
sudo tar -czvf pips.tar.gz pips

cp save.tar.gz fmyar-diploma-test
cp jovyan.tar.gz fmyar-diploma-test
cp pips.tar.gz fmyar-diploma-test
```

#### VM2

запускаем докер образ jupyter-lab с нужными флагами, и в старте делаем /bin/true, это нужно для того чтобы создать контейнер с нужными volume.

```shell
sudo docker run  --user root -v ~/jovyan:/home/jovyan/ -v ~/pips:/pips -e CHOWN_HOME=yes -e CHOWN_HOME_OPTS='-R' -e CHOWN_EXTRA="/pips" -e PYTHONPATH="/pips" --name jupyter -p 8888:8888 jupyter/scipy-notebook /bin/true
```

(делаем из под рута)

Копируем файлы с s3, и разархивируем их

```shell
cp fmyar-diploma-test/jovyan.tar.gz .
cp fmyar-diploma-test/save.tar.gz .
cp fmyar-diploma-test/pips.tar.gz .

sudo tar -xzvf save.tar.gz 
sudo tar -xzvf jovyan.tar.gz 
sudo tar -xzvf pips.tar.gz
```

нужно скопировать чекпоинт в директорию с чекпоинтами у образа

```shell
cp -r ./checkpoint/save /var/lib/docker/containers/{jupyterlab_container_id}/checkpoints/
```

проверяем что чекпоинт появился

```shell
docker checkpoint ls jupyter
```

запускаем контейнер с нужным чекпоинтом

```shell
docker start --checkpoint save jupyter
```

можем заходить в jupyter-lab и проверять что состояние перенеслось.