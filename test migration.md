### Image migaration (ok)
```python
from PIL import Image
img = Image.open('img.png')
/kernel/lib/python3.7/site-packages/ml_kernel/kernel.py:828: UserWarning: The following variables cannot be serialized: img
warnings.warn(message)
```

### Fasttext migration (ok)
```python
!wget https://dl.fbaipublicfiles.com/fasttext/data/cooking.stackexchange.tar.gz && tar xvzf cooking.stackexchange.tar.gz
!head -n 12404 cooking.stackexchange.txt > cooking.train
!tail -n 3000 cooking.stackexchange.txt > cooking.valid

%pip install fasttext

import fasttext

model = fasttext.train_supervised(input="cooking.train")
```

### Files descriptors
```python
f = open('file.txt', 'r')
f.readline()
f.readline()
```

перенос 

### Toloka-kit (ok)
```python
%pip install toloka-kit==0.1.10

import toloka.client as toloka
pool = toloka.pool.Pool()
# закрытие проекта
pool
```

### sklearn regression (ok)
```python
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

# Load the diabetes dataset
diabetes_X, diabetes_y = datasets.load_diabetes(return_X_y=True)

# Use only one feature
diabetes_X = diabetes_X[:, np.newaxis, 2]

# Split the data into training/testing sets
diabetes_X_train = diabetes_X[:-20]
diabetes_X_test = diabetes_X[-20:]

# Split the targets into training/testing sets
diabetes_y_train = diabetes_y[:-20]
diabetes_y_test = diabetes_y[-20:]

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(diabetes_X_train, diabetes_y_train)





diabetes_y_pred = regr.predict(diabetes_X_test)

# The coefficients
print("Coefficients: \n", regr.coef_)
# The mean squared error
print("Mean squared error: %.2f" % mean_squared_error(diabetes_y_test, diabetes_y_pred))
# The coefficient of determination: 1 is perfect prediction
print("Coefficient of determination: %.2f" % r2_score(diabetes_y_test, diabetes_y_pred))

# Plot outputs
plt.scatter(diabetes_X_test, diabetes_y_test, color="black")
plt.plot(diabetes_X_test, diabetes_y_pred, color="blue", linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()
```



### grpc (ok)
`sudo pip install grpcio grpcio-tools`

`sudo nano bidirectional.proto`

```protobuf
syntax = "proto3";

package grpc;

message Empty {}


message Note {
    string name = 1;
    string message = 2;
}

message Res {
    int32 res = 1;
}

service ChatServer {
    rpc ChatStream (Empty) returns (stream Note);
    rpc SendNote (Note) returns (Res);
}
```

`sudo python3 -m grpc_tools.protoc --proto_path=.  ./bidirectional.proto --python_out=. --grpc_python_out=.`

```python
import logging
from concurrent import futures

import grpc

import bidirectional_pb2
import bidirectional_pb2_grpc


class BidirectionalService(bidirectional_pb2_grpc.ChatServerServicer):
    def __init__(self):
        self.chats = []
        self.ind = 0

    def ChatStream(self, request_iterator, context):
        lastindex = 0
        while True:
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n

    def SendNote(self, request: bidirectional_pb2.Note, context):
        print("[{}] {}".format(request.name, request.message))
        self.chats.append(request)
        res = bidirectional_pb2.Res()
        res.res = self.ind
        self.ind += 1
        return res


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bidirectional_pb2_grpc.add_ChatServerServicer_to_server(BidirectionalService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

```

* tcp-close -- работает, в плане запрос - ответ, перенос запрос - ответ, заново канал не открываем. но при стрименге итератор next выдает:
```
_MultiThreadedRendezvous: <_MultiThreadedRendezvous of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "Socket closed"
	debug_error_string = "UNKNOWN:Error received from peer ipv4:158.160.4.227:50051 {created_time:"2023-04-30T17:12:16.98428025+00:00", grpc_status:14, grpc_message:"Socket closed"}"
>
``` 
надо заново переоткрывать стрим

похожая ошибка при tcp-established в случае стрима

```
_MultiThreadedRendezvous: <_MultiThreadedRendezvous of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "recvmsg:Connection reset by peer"
	debug_error_string = "UNKNOWN:Error received from peer ipv4:158.160.4.227:50051 {grpc_message:"recvmsg:Connection reset by peer", grpc_status:14, created_time:"2023-04-30T22:28:42.424122289+00:00"}"
```

### sqlite

```python
import sqlite3
import pandas
conn = sqlite3.connect(':memory:')
df = pandas.read_csv('accessories.csv')
r = df.to_sql('usage', conn, if_exists='replace', index=False)
cursor = conn.cursor()
cursor.execute('select * from usage')
cursor.fetchone()
cursor.fetchone()
cursor.fetchone()
```




### data more than ram in second vm
1 vm: 4gb ram 2vcpu.

2 vm: 2gb ram 2vcpu.

state 3273.284996032715 (not ok)

```python3
x = [1 for _ in range(3 * 1024 * 1024 * 1024 // 8)]
import sys
sys.getsizeof(x) / 1024 / 1024
```

state 2298.9325790405273 (not ok) https://gist.github.com/FMyb/16817f4e16dbc068f02692525823ca74

```python3
x = [1 for _ in range(2 * 1024 * 1024 * 1024 // 8)]
import sys
sys.getsizeof(x) / 1024 / 1024
```

# data usage coef

before data usage
```
               total        used        free      shared  buff/cache   available
Mem:           1.9Gi       399Mi       1.2Gi       1.0Mi       373Mi       1.4Gi
Swap:             0B          0B          0B
Total:         1.9Gi       399Mi       1.2Gi
```

docker stats
```
CONTAINER ID   NAME      CPU %     MEM USAGE / LIMIT     MEM %     NET I/O         BLOCK I/O        PIDS
6ddfe1d61769   jupyter   0.01%     196.6MiB / 1.928GiB   9.95%     133kB / 363kB   93.8MB / 197kB   20
```

```python3
x = [1 for _ in range(int(1.3 * 1024 * 1024 * 1024 // 8))]
import sys
sys.getsizeof(x) / 1024 / 1024
```
### 1435.2122116088867mb

after data usage
```
               total        used        free      shared  buff/cache   available
Mem:           1.9Gi       1.7Gi        79Mi       1.0Mi       171Mi        97Mi
Swap:             0B          0B          0B
Total:         1.9Gi       1.7Gi        79Mi
```

docker stats
```
CONTAINER ID   NAME      CPU %     MEM USAGE / LIMIT     MEM %     NET I/O         BLOCK I/O       PIDS
6ddfe1d61769   jupyter   0.05%     1.463GiB / 1.928GiB   75.84%    412kB / 653kB   406MB / 500kB   20
```

### fail

```python3
x = [1 for _ in range(int(1.15 * 1024 * 1024 * 1024 // 8))]
import sys
sys.getsizeof(x) / 1024 / 1024
```

### 1275.7441635131836 mb

after data usage
```
               total        used        free      shared  buff/cache   available
Mem:         2022120     1608308       78164        1264      335648      243452
Swap:              0           0           0
Total:       2022120     1608308       78164
```
```
               total        used        free      shared  buff/cache   available
Mem:           1.9Gi       1.5Gi        69Mi       1.0Mi       327Mi       231Mi
Swap:             0B          0B          0B
Total:         1.9Gi       1.5Gi        69Mi
```

docker stats
```
CONTAINER ID   NAME      CPU %     MEM USAGE / LIMIT     MEM %     NET I/O         BLOCK I/O        PIDS
bd2e5c96e36b   jupyter   0.13%     1.323GiB / 1.928GiB   68.60%    153kB / 384kB   87.1MB / 233kB   20
```

https://gist.github.com/FMyb/2eeb4ed1fe5bad930448a1cff1473300

### ok

```python3
x = [1 for _ in range(int(1024 * 1024 * 1024 // 8))]
import sys
sys.getsizeof(x) / 1024 / 1024
```

### 1133.994773864746mb

after data usage
```
               total        used        free      shared  buff/cache   available
Mem:         2022120     1462448       71896        1264      487776      364380
Swap:              0           0           0
Total:       2022120     1462448       71896
```

```
               total        used        free      shared  buff/cache   available
Mem:           1.9Gi       1.4Gi        69Mi       1.0Mi       476Mi       355Mi
Swap:             0B          0B          0B
Total:         1.9Gi       1.4Gi        69Mi
```

docker stats
```
CONTAINER ID   NAME      CPU %     MEM USAGE / LIMIT     MEM %     NET I/O         BLOCK I/O        PIDS
52fb2335497e   jupyter   0.01%     1.164GiB / 1.928GiB   60.35%    198kB / 421kB   66.7MB / 233kB   20
```

### ok



before usage
```
               total        used        free      shared  buff/cache   available
Mem:         4017120      464136      306068        1260     3246916     3249500
Swap:              0           0           0
Total:       4017120      464136      306068
```

after usage
```
               total        used        free      shared  buff/cache   available
Mem:         4017120     3494328      156484        1260      366308      249824
Swap:              0           0           0
Total:       4017120     3494328      156484
```

### 3273.284996032715

fail to restore

```
Error response from daemon: failed to upload checkpoint to containerd: failed to send write: write /var/lib/containerd/io.containerd.content.v1.content/ingest/13a554e610dd23ceb908aa4411d34fbf2871c6f394aa868323ceb53bd7b50245/data: no space left on device: unknown
```

https://gist.github.com/FMyb/e0e2cf41ddf0a597d5d71f7f83aa1e9c -- vm 1
https://gist.github.com/FMyb/027d7373412e23550895a4dc60e0e031 -- vm 2


with swap

before usage
```
               total        used        free      shared  buff/cache   available
Mem:         4017120      404520      176348        1264     3436252     3309112
Swap:              0           0           0
Total:       4017120      404520      176348
```

after usage
```
               total        used        free      shared  buff/cache   available
Mem:         4017120     3072500      133040        1268      811580      641128
Swap:              0           0           0
Total:       4017120     3072500      133040
```

```python3
x = [1 for _ in range(int(2.5 * 1024 * 1024 * 1024 / 8))]
import sys
sys.getsizeof(x) / 1024 / 1024
```

### 2586.299186706543

https://gist.github.com/FMyb/4b7b5efa060452ff1fceaad2d076eaf9 -- vm 1
https://gist.github.com/FMyb/b4f7de81624d8cfe41995968c7538b61 -- vm 2

```
result time: 0:17:55.715997
docker checkpoint create: 0:06:37.119887
tar time: 0:01:17.738653
cp time: 0:00:01.923975
restore time (with http request): 0:09:58.933478
b'result time: 0:09:58.917370\ncp tar time: 0:00:00.499080\ntar time: 0:00:24.423981\ncp checkpoint time: 0:02:17.542655\ndocker start time: 0:07:16.451646'
checkpoint size=2821856471
checkpoint compress size=34970053
jovyan compress size=5160
```
```
{'usage': 2906255360, 'stats': {'active_anon': 24576, 'active_file': 40419328, 'anon': 2829938688, 'anon_thp': 0, 'file': 62046208, 'file_dirty': 0, 'file_mapped': 20508672, 'file_writeback': 0, 'inactive_anon': 2829897728, 'inactive_file': 21626880, 'kernel_stack': 344064, 'pgactivate': 17966, 'pgdeactivate': 8962, 'pgfault': 1000796, 'pglazyfree': 0, 'pglazyfreed': 0, 'pgmajfault': 484, 'pgrefill': 13869, 'pgscan': 15553, 'pgsteal': 10462, 'shmem': 0, 'slab': 7592976, 'slab_reclaimable': 6745760, 'slab_unreclaimable': 847216, 'sock': 16384, 'thp_collapse_alloc': 0, 'thp_fault_alloc': 0, 'unevictable': 0, 'workingset_activate': 0, 'workingset_nodereclaim': 0, 'workingset_refault': 0}, 'limit': 4113530880}
```

2 cpu 4 ram 64 hdd
```python
x = [1 for _ in range(int(3.5 * 1024 * 1024 * 1024 / 8))]
import sys
sys.getsizeof(x) / 1024 / 1024
```

after usage
```
               total        used        free      shared  buff/cache   available
Mem:         4017120     3758260      116936        1264      141924       58468
Swap:              0           0           0
Total:       4017120     3758260      116936
```

### 3682.445640563965 mb

https://gist.github.com/FMyb/28035b5a6207d79104b09235d34f1ad5 -- vm 1
https://gist.github.com/FMyb/6314a3cb66ab696bfb22187da7347bb0 -- vm 2

```
result time: 0:25:31.590308
docker checkpoint create: 0:08:19.276512
tar time: 0:02:05.427757
cp time: 0:00:03.073062
restore time (with http request): 0:15:03.812972
b'result time: 0:15:03.736480\ncp tar time: 0:00:00.422258\ntar time: 0:00:31.665147\ncp checkpoint time: 0:03:25.416234\ndocker start time: 0:11:06.229267'
checkpoint size=3573233770
checkpoint compress size=36021821
jovyan compress size=5205
```
```
{'usage': 3602546688, 'stats': {'active_anon': 12288, 'active_file': 14520320, 'anon': 3573030912, 'anon_thp': 0, 'file': 19132416, 'file_dirty': 0, 'file_mapped': 10731520, 'file_writeback': 0, 'inactive_anon': 3573018624, 'inactive_file': 4612096, 'kernel_stack': 327680, 'pgactivate': 31699, 'pgdeactivate': 34494, 'pgfault': 2265876, 'pglazyfree': 0, 'pglazyfreed': 0, 'pgmajfault': 1112, 'pgrefill': 49267, 'pgscan': 258903, 'pgsteal': 44307, 'shmem': 0, 'slab': 2514568, 'slab_reclaimable': 1768056, 'slab_unreclaimable': 746512, 'sock': 16384, 'thp_collapse_alloc': 0, 'thp_fault_alloc': 0, 'unevictable': 0, 'workingset_activate': 0, 'workingset_nodereclaim': 0, 'workingset_refault': 0}, 'limit': 4113530880}
```

ok

4 cpu 4 ram 64 hdd
before
```
               total        used        free      shared  buff/cache   available
Mem:         4016648      462628      163712        1276     3390308     3250696
Swap:              0           0           0
Total:       4016648      462628      163712
```

```python
x = [1 for _ in range(int(3.2 * 1024 * 1024 * 1024 / 8))]
import sys
sys.getsizeof(x) / 1024 / 1024
```

after
```
               total        used        free      shared  buff/cache   available
Mem:         4016648     3783136      140268        1276       93244       57676
Swap:              0           0           0
Total:       4016648     3783136      140268
```

### 3682.445640563965 mb

fail vm 1


4 cpu 4 ram 64 hdd
before
```
               total        used        free      shared  buff/cache   available
Mem:         4016648      462628      163712        1276     3390308     3250696
Swap:              0           0           0
Total:       4016648      462628      163712
```

```python
x = [1 for _ in range(int(3.1 * 1024 * 1024 * 1024 / 8))]
import sys
sys.getsizeof(x) / 1024 / 1024
```

after
```
               total        used        free      shared  buff/cache   available
Mem:         4016640     3725964      139068        1288      151608       85260
Swap:              0           0           0
Total:       4016640     3725964      139068
```

### 3273.284996032715 mb

fail vm 1


```python
x = [1 for _ in range(int(3 * 1024 * 1024 * 1024 / 8))]
import sys
sys.getsizeof(x) / 1024 / 1024
```

```
               total        used        free      shared  buff/cache   available
Mem:         4016640     3630980      140764        1288      244896      133812
Swap:              0           0           0
Total:       4016640     3630980      140764
```

### 3273.284996032715 mb

https://gist.github.com/FMyb/8cdde8b9a5ea9d4ddaed20d64e2f0113 -- vm 1
https://gist.github.com/FMyb/a5a05401b8e84a5c1933ddb54729c5e6 -- vm 2

```
{'usage': 3392462848, 'stats': {'active_anon': 12288, 'active_file': 16592896, 'anon': 3358580736, 'anon_thp': 0, 'file': 23965696, 'file_dirty': 0, 'file_mapped': 5857280, 'file_writeback': 0, 'inactive_anon': 3358568448, 'inactive_file': 7372800, 'kernel_stack': 327680, 'pgactivate': 21552, 'pgdeactivate': 20249, 'pgfault': 1032844, 'pglazyfree': 0, 'pglazyfreed': 0, 'pgmajfault': 643, 'pgrefill': 27099, 'pgscan': 26474, 'pgsteal': 24349, 'shmem': 0, 'slab': 2489168, 'slab_reclaimable': 1738680, 'slab_unreclaimable': 750488, 'sock': 16384, 'thp_collapse_alloc': 0, 'thp_fault_alloc': 0, 'unevictable': 0, 'workingset_activate': 0, 'workingset_nodereclaim': 0, 'workingset_refault': 0}, 'limit': 4113039360}
```

```
result time: 0:35:32.913519
docker checkpoint create: 0:13:16.150755
tar time: 0:04:30.212502
cp time: 0:00:02.213038
restore time (with http request): 0:17:44.337219
b'result time: 0:17:44.289245\ncp tar time: 0:00:00.522792\ntar time: 0:00:36.509802\ncp checkpoint time: 0:04:45.950217\ndocker start time: 0:12:21.304730'
checkpoint size=3358782223
checkpoint compress size=35749752
jovyan compress size=5148
```

ok


## 4cpu 8 ram 64 hdd
```
CONTAINER ID   NAME      CPU %     MEM USAGE / LIMIT     MEM %     NET I/O          BLOCK I/O        PIDS
3f88fe2838a6   jupyter   0.01%     167.1MiB / 7.762GiB   2.10%     1.3GB / 26.6MB   12.9MB / 939MB   20
```

```
               total        used        free      shared  buff/cache   available
Mem:         8139268      497148     4193444        1272     3448676     7322480
Swap:              0           0           0
Total:       8139268      497148     4193444
```
```python
import pandas as pd
df = pd.read_csv('custom_2017_2020.csv')
df.head()
```
```python
b = df.memory_usage(index=True).sum()
b / 1024 / 1024
```

### 1477.5361328125 mb

```
{'usage': 2717540352, 'stats': {'active_anon': 16384, 'active_file': 131072, 'anon': 1726914560, 'anon_thp': 1539309568, 'file': 950149120, 'file_dirty': 0, 'file_mapped': 397312, 'file_writeback': 0, 'inactive_anon': 1726898176, 'inactive_file': 950018048, 'kernel_stack': 458752, 'pgactivate': 42, 'pgdeactivate': 0, 'pgfault': 1680535, 'pglazyfree': 0, 'pglazyfreed': 0, 'pgmajfault': 30, 'pgrefill': 0, 'pgscan': 448, 'pgsteal': 422, 'shmem': 0, 'slab': 35874112, 'slab_reclaimable': 34789264, 'slab_unreclaimable': 1084848, 'sock': 12288, 'thp_collapse_alloc': 0, 'thp_fault_alloc': 1459, 'unevictable': 0, 'workingset_activate': 0, 'workingset_nodereclaim': 0, 'workingset_refault': 0}, 'limit': 8334610432}
```
https://gist.github.com/FMyb/72c0989f785bf670a4d892d4bdc83521 - vm1
https://gist.github.com/FMyb/961f350a730869d672c926f0ded01e5e - vm2

```
result time: 0:03:45.525872
docker checkpoint create: 0:00:53.720633
tar time: 0:01:19.853275
cp time: 0:00:07.617319
restore time (with http request): 0:01:24.334641
b'result time: 0:01:24.328976\ncp tar time: 0:00:04.152265\ntar time: 0:00:16.822598\ncp checkpoint time: 0:00:14.295352\ndocker start time: 0:00:49.058710'
checkpoint size=1727163669
checkpoint compress size=167521897
jovyan compress size=164439491
```
ok


## 2cpu 2ram 64hdd

```
CONTAINER ID   NAME      CPU %     MEM USAGE / LIMIT     MEM %     NET I/O          BLOCK I/O        PIDS
12d0d6c5e8cf   jupyter   1.36%     200.8MiB / 1.928GiB   10.17%    639MB / 12.7MB   65.1MB / 463MB   20
```
```
               total        used        free      shared  buff/cache   available
Mem:         2022120      426956      783588        1264      811576     1429040
Swap:              0           0           0
Total:       2022120      426956      783588
```
```python
import pandas as pd
df = pd.read_csv('y_1997.csv')
df.head()
```
```python
import sys
b = sys.getsizeof(df)
b / 1024 / 1024
```

### 1477.5361328125 mb















sudo docker checkpoint rm --checkpoint-dir /home/yarusha/checkpoint jupyter save
sudo docker stop jupyter
sudo docker rm jupyter
rm -r jovyan
rm -r pips
sudo docker run --user root -v ~/jovyan:/home/jovyan/ -e CHOWN_HOME=yes -e CHOWN_HOME_OPTS='-R'  --name jupyter -p 8888:8888  jupyter/scipy-notebook start-notebook.sh --NotebookNotary.db_file=:memory:
