import subprocess
import requests
from datetime import datetime
from pathlib import Path

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


def check_process(process: subprocess.CompletedProcess):
    print('STDOUT:', process.stdout)
    if process.returncode != 0:
        print('STDERR:', process.stderr)
        exit(process.returncode)


def execute_string(command: str):
    print('run command:', command)
    process = subprocess.run(command.split())
    check_process(process)


second_vm_ip = input('second vm ip:')

use_custom = False if input('Use custom settings [Enter for no, something else for yes]: ') == '' else True

def_jovyan_volume = '/home/yarusha/jovyan'
jovyan_volume = ''
def_s3_mount = '/home/yarusha/fmyar-diploma-test'
s3_mount = ''
def_dump_file = 'dump.cpkl'
dump_file = ''

if use_custom:
    jovyan_volume = input(f'jovyan volume [default: {def_jovyan_volume}]: ')
    s3_mount = input(f's3 mount [default: {def_s3_mount}]: ')
    dump_file = input(f'dump file [default: {def_dump_file}]: ')

if jovyan_volume == '':
    jovyan_volume = def_jovyan_volume
if s3_mount == '':
    s3_mount = def_s3_mount
if dump_file == '':
    dump_file = def_dump_file

ram()
start_time_all = datetime.now()

execute_string(f"docker exec -it jupyter jupyter nbconvert --to notebook --execute --inplace Untitled.ipynb")

docker_exec_time = datetime.now()
ram()

execute_string(f"cp {jovyan_volume}/{dump_file} {s3_mount}")

cp_time = datetime.now()

resp = requests.post(f'http://{second_vm_ip}:8080', json={'dump_file': dump_file})

finish_dump = datetime.now()

print(f'docker time: {docker_exec_time - start_time_all}')
print(f'cp time: {cp_time - docker_exec_time}')
print(f'all time: {finish_dump - start_time_all}')

if resp.status_code != 200:
    print(f'error, status code: {resp.status_code}')
    print(resp.content)
    exit(1)
print(resp.content)

print(f"dump size={Path(jovyan_volume).joinpath(dump_file).stat().st_size}")
