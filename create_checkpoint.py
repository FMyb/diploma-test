import subprocess
import os
import docker


def check_process(process: subprocess.CompletedProcess):
    if process.returncode != 0:
        exit(process.returncode)


def execute_string(command: str):
    process = subprocess.run(command.split())
    check_process(process)



use_custom = False if input('Use custom settings [Enter for no, something else for yes]: ') == '' else True

def_docker_image_name = 'jupyter'
docker_image_name = ''
def_checkpoint_name = 'save'
checkpoint_name = ''

if use_custom:
    docker_image_name = input(f'docker image name [default: {def_docker_image_name}]: ')
    checkpoint_name = input(f'checkpoint name [default: {def_checkpoint_name}]: ')
if docker_image_name == '':
    docker_image_name = def_docker_image_name
if checkpoint_name == '':
    checkpoint_name = def_checkpoint_name

docker_container = None
print(f'Find container with name: {docker_image_name}')
client = docker.client.from_env()
for _container in client.containers.list(all=True):
    if _container.name == docker_image_name:
        docker_container = _container
if docker_container is None:
    print(f'Unable to find container with name: {docker_image_name}')
    exit(1)

execute_string(f'docker checkpoint create {docker_image_name} {checkpoint_name}')

print('Created.')
