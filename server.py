import flask
import docker
import subprocess
from datetime import datetime


def check_process(process: subprocess.CompletedProcess):
    print('STDOUT:', process.stdout)
    if process.returncode != 0:
        print('STDERR:', process.stderr)
        exit(process.returncode)


def execute_string(command: str):
    print('run command:', command)
    process = subprocess.run(command.split())
    check_process(process)


app = flask.Flask(__name__)

def_home = '/home/yarusha'
home = ''
def_s3_mount = '/home/yarusha/fmyar-diploma-test'
s3_mount = ''
def_docker_image_name = 'jupyter'
docker_image_name = ''
def_checkpoint_dir = '/home/yarusha/checkpoint'
checkpoint_dir = ''
def_pip_dir = '/home/yarusha/pips'
pip_dir = ''
docker_container = None

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


def init():
    global s3_mount
    global docker_image_name
    global docker_container
    global home
    global checkpoint_dir
    global pip_dir

    use_custom = False if input('Use custom settings [Enter for no, something else for yes]: ') == '' else True
    if use_custom:
        checkpoint_dir = input(f'checkpoint_dir [default: {def_checkpoint_dir}]: ')
        docker_image_name = input(f'docker image name [default: {def_docker_image_name}]: ')
        s3_mount = input(f's3 mount [default: {def_s3_mount}]: ')
        home = input(f'home [default: {def_home}]: ')
        pip_dir = input(f'pip dir [default: {def_pip_dir}]: ')

    if docker_image_name == '':
        docker_image_name = def_docker_image_name
    if s3_mount == '':
        s3_mount = def_s3_mount
    if home == '':
        home = def_home
    if checkpoint_dir == '':
        checkpoint_dir = def_checkpoint_dir
    if pip_dir == '':
        pip_dir = def_pip_dir

    print(f'Find container with name: {docker_image_name}')
    client = docker.client.from_env()
    for _container in client.containers.list(all=True):
        if _container.name == docker_image_name:
            docker_container = _container
    if docker_container is None:
        print(f'Unable to find container with name: {docker_image_name}')
        exit(1)


@app.route('/', methods=['POST'])
def process():
    if flask.request.method == 'POST':
        data = flask.request.get_json()
        checkpoint_name = data['checkpoint_name']
        start_time_all = datetime.now()
        execute_string(f'cp {s3_mount}/jovyan.tar.gz {home}')
        execute_string(f'cp {s3_mount}/{checkpoint_name}.tar.gz {home}')
        execute_string(f'cp {s3_mount}/pips.tar.gz {home}')
        finish_cp = datetime.now()
        execute_string(f'sudo tar -xzvf {checkpoint_name}.tar.gz')
        execute_string(f'sudo tar -xzvf jovyan.tar.gz')
        execute_string(f'sudo tar -xzvf pips.tar.gz')
        finish_tar = datetime.now()
        execute_string(
            f'cp -r {checkpoint_dir}/{checkpoint_name} /var/lib/docker/containers/{docker_container.id}/checkpoints/'
        )
        ram()
        finish_cp_checkpoint = datetime.now()
        execute_string(f'docker start --checkpoint {checkpoint_name} {docker_image_name}')
        finish_restore = datetime.now()
        ram()
        ans = f"result time: {datetime.now() - start_time_all}\ncp tar time: {finish_cp - start_time_all}\ntar time: " \
              f"{finish_tar - finish_cp}\ncp checkpoint time: {finish_cp_checkpoint - finish_tar}\ndocker start time: {finish_restore - finish_cp_checkpoint}"
        return ans


if __name__ == '__main__':
    # run app in debug mode on port 5000
    init()
    app.run(host='0.0.0.0', port=8080)
