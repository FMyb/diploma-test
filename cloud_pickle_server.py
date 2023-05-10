import flask
import subprocess
from datetime import datetime

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


app = flask.Flask(__name__)

def_jovyan_volume = '/home/yarusha/jovyan'
jovyan_volume = ''
def_s3_mount = '/home/yarusha/fmyar-diploma-test'
s3_mount = ''


def init():
    global s3_mount
    global jovyan_volume

    use_custom = False if input('Use custom settings [Enter for no, something else for yes]: ') == '' else True
    if use_custom:
        jovyan_volume = input(f'jovyan volume [default: {def_jovyan_volume}]: ')
        s3_mount = input(f's3 mount [default: {def_s3_mount}]: ')

    if jovyan_volume == '':
        jovyan_volume = def_jovyan_volume
    if s3_mount == '':
        s3_mount = def_s3_mount


@app.route('/', methods=['POST'])
def process():
    if flask.request.method == 'POST':
        data = flask.request.get_json()
        dump_file = data['dump_file']
        start_time_all = datetime.now()
        execute_string(f'cp {s3_mount}/{dump_file} {jovyan_volume}')
        ram()
        finish_cp = datetime.now()
        execute_string(
            f' sudo docker exec -it jupyter jupyter nbconvert --to python --execute --inplace Untitled.ipynb')
        finish_restore = datetime.now()
        ram()
        ans = f"result time second vm: {datetime.now() - start_time_all}\ncp time second vm: {finish_cp - start_time_all}\nrestore time: {finish_restore - finish_cp}"
        return ans


if __name__ == '__main__':
    # run app in debug mode on port 5000
    init()
    app.run(host='0.0.0.0', port=8080)
