import subprocess

import requests
from datetime import datetime
import os
from pathlib import Path
import docker


def check_process(process: subprocess.CompletedProcess):
    print('STDOUT:', process.stdout)
    if process.returncode != 0:
        print('STDERR:', process.stderr)
        exit(process.returncode)


def execute_string(command: str):
    print('run command:', command)
    process = subprocess.run(command.split())
    check_process(process)


ramF = True
proc = None
file = None
def ram():
    global ramF
    global proc
    global file
    if ramF:
        file = open('ram.log', 'w')
        proc = subprocess.Popen(['free', '-t', '-s', '1'], universal_newlines=True, stdout=file)
        ramF = False
    else:
        ramF = True
        proc.terminate()
        file.close()


second_vm_ip = input('second vm ip:')

use_custom = False if input('Use custom settings [Enter for no, something else for yes]: ') == '' else True

def_checkpoint_dir = '/home/yarusha/checkpoint'
checkpoint_dir = ''
def_docker_image_name = 'jupyter'
docker_image_name = ''
def_checkpoint_name = 'save'
checkpoint_name = ''
def_jovyan_volume = '/home/yarusha/jovyan'
jovyan_volume = ''
def_s3_mount = '/home/yarusha/fmyar-diploma-test'
s3_mount = ''
def_pip_dir = '/home/yarusha/pips'
pip_dir = ''
cur_dir = os.path.dirname(__file__)

if use_custom:
    checkpoint_dir = input(f'checkpoint_dir [default: {def_checkpoint_dir}]: ')
    docker_image_name = input(f'docker image name [default: {def_docker_image_name}]: ')
    checkpoint_name = input(f'checkpoint name [default: {def_checkpoint_name}]: ')
    jovyan_volume = input(f'jovyan volume [default: {def_jovyan_volume}]: ')
    s3_mount = input(f's3 mount [default: {def_s3_mount}]: ')
    pip_dir = input(f'pip dir [default: {def_pip_dir}]: ')
if checkpoint_dir == '':
    checkpoint_dir = def_checkpoint_dir
if docker_image_name == '':
    docker_image_name = def_docker_image_name
if checkpoint_name == '':
    checkpoint_name = def_checkpoint_name
if jovyan_volume == '':
    jovyan_volume = def_jovyan_volume
if s3_mount == '':
    s3_mount = def_s3_mount
if pip_dir == '':
    pip_dir = def_pip_dir

docker_container = None
print(f'Find container with name: {docker_image_name}')
client = docker.client.from_env()
for _container in client.containers.list(all=True):
    if _container.name == docker_image_name:
        docker_container = _container
if docker_container is None:
    print(f'Unable to find container with name: {docker_image_name}')
    exit(1)

print(docker_container.stats(stream=False)['memory_stats'])

ram()
start_time_all = datetime.now()

execute_string(f'docker checkpoint create --checkpoint-dir {checkpoint_dir} {docker_image_name} {checkpoint_name}')

finish_docker_checkpoint_create = datetime.now()
ram()

checkpoint_full_path = Path(checkpoint_dir).joinpath(Path(checkpoint_name))

execute_string(
    f'tar -czvf {checkpoint_name}.tar.gz {os.path.relpath(checkpoint_dir, cur_dir)}/{checkpoint_name}'
)

execute_string(f'tar -czvf jovyan.tar.gz {os.path.relpath(jovyan_volume, cur_dir)}')

execute_string(f'sudo tar -czvf pips.tar.gz {os.path.relpath(pip_dir, cur_dir)}')

finish_tar = datetime.now()

execute_string(f'cp {checkpoint_name}.tar.gz {s3_mount}')
execute_string(f'cp jovyan.tar.gz {s3_mount}')
execute_string(f'cp pips.tar.gz {s3_mount}')

finish_cp = datetime.now()

resp = requests.post(f'http://{second_vm_ip}:8080', json={'checkpoint_name': checkpoint_name})

finish_restore = datetime.now()

print('result time:', datetime.now() - start_time_all)
print('docker checkpoint create:', finish_docker_checkpoint_create - start_time_all)
print('tar time:', finish_tar - finish_docker_checkpoint_create)
print('cp time:', finish_cp - finish_tar)
print('restore time (with http request):', finish_restore - finish_cp)

if resp.status_code != 200:
    print(f'error, status code: {resp.status_code}')
    print(resp.content)
    exit(1)
print(resp.content)

print(f"checkpoint size={sum(f.stat().st_size for f in checkpoint_full_path.glob('**/*') if f.is_file())}")
print(f"checkpoint compress size={Path(f'{checkpoint_name}.tar.gz').stat().st_size}")
print(f"jovyan compress size={Path('jovyan.tar.gz').stat().st_size}")
