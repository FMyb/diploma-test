import flask
import docker
import tarfile
import os.path
import os
import boto3
from pathlib import Path
import json


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def uncompress(source_filename, dest_dir):
    with tarfile.open(source_filename, "r:gz") as tar:
        tar.extractall(dest_dir)


def checkpoint_path(checkpoint_name, checkpoint_dir=None) -> Path:
    if checkpoint_dir is not None:
        return Path(checkpoint_dir, checkpoint_name)
    else:
        return Path("/var/lib/docker/containers/", docker_container.id, "checkpoints", checkpoint_name)


docker_container = None
client = docker.client.from_env()
session = None
s3 = None
s3_bucket_name = 'fmyar-diploma-test'
s3_files_prefix = 'checkpoints'
jovyan_path = Path("/home/yarusha/jovyan")
libraries_path = Path("/home/yarusha/pips")
cur_dir = os.path.dirname(__file__)


def prepare():
    global docker_container
    global client
    global session
    global s3
    print('find docker container')
    for _container in client.containers.list(all=True):
        if _container.name == 'jupyter':
            docker_container = _container
    if docker_container is None:
        print('Failed to find docker container with name jupyter')
        exit(1)
    print('docker container found')
    print('connect to s3')
    aws_access_key_id = os.environ['AWSACCESSKEYID']
    if aws_access_key_id.strip() == '':
        print('AWSACCESSKEYID not correct')
    aws_secret_access_key = os.environ['AWSSECRETACCESSKEY']
    if aws_secret_access_key.strip() == '':
        print('AWSSECRETACCESSKEY not correct')
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net'
    )
    print('connected to s3')


def archive_and_upload(s3_cur_dir, archive_file, path):
    print(f'archive: {path} -> {archive_file}')
    make_tarfile(archive_file, path)
    print(f'done')
    print(f'upload: {archive_file} -> {s3_bucket_name}/{s3_cur_dir}/{archive_file}')
    s3.upload_file(
        archive_file,
        s3_bucket_name,
        f'{s3_cur_dir}/{archive_file}'
    )
    print('done')


def download_and_unarchive(s3_cur_dir, archive_file, path):
    print(f'download: {s3_bucket_name}/{s3_cur_dir}/{archive_file} -> {archive_file}')
    s3.download_file(
        s3_bucket_name,
        f'{s3_cur_dir}/{archive_file}',
        archive_file
    )
    print('done')
    print(f'uncompress: {archive_file} -> {path}')
    uncompress(archive_file, path)
    print('done')


app = flask.Flask(__name__)


@app.route('/save_state', methods=['POST'])
def save_state():
    if flask.request.method == 'POST':
        data = flask.request.get_json()
        checkpoint_name = data['checkpointName']

        print(f'create checkpoint {checkpoint_name}')
        s3_cur_dir = f'{s3_files_prefix}/{checkpoint_name}'

        work_directory_archive_file = "jovyan.tar.gz"
        archive_and_upload(s3_cur_dir, work_directory_archive_file, os.path.relpath(jovyan_path, cur_dir))

        libraries_archive_file = "pips.tar.gz"
        archive_and_upload(s3_cur_dir, libraries_archive_file, os.path.relpath(libraries_path, cur_dir))

        print(f'create checkpoint')
        client.api.container_create_checkpoint(docker_container.id, checkpoint_name, leave_running=True)
        print('done')
        checkpoint_archive_file = f"{checkpoint_name}.tar.gz"
        archive_and_upload(
            s3_cur_dir,
            checkpoint_archive_file,
            os.path.relpath(checkpoint_path(checkpoint_name), cur_dir)
        )
        print(f'create checkpoint {checkpoint_name} done')
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/load_state', methods=['POST'])
def load_state():
    if flask.request.method == 'POST':
        data = flask.request.get_json()
        checkpoint_name = data['checkpointName']
        print(f'load checkpoint {checkpoint_name}')
        s3_cur_dir = f'{s3_files_prefix}/{checkpoint_name}'

        if docker_container.attrs["State"]["Status"] == "running":
            client.api.stop(docker_container.id)

        work_directory_archive_file = "jovyan.tar.gz"
        download_and_unarchive(s3_cur_dir, work_directory_archive_file, jovyan_path.parent)

        libraries_archive_file = "pips.tar.gz"
        download_and_unarchive(s3_cur_dir, libraries_archive_file, libraries_path.parent)

        checkpoint_archive_file = f"{checkpoint_name}.tar.gz"
        download_and_unarchive(s3_cur_dir, checkpoint_archive_file, checkpoint_path(checkpoint_name).parent)
        print(f'start container')
        client.api.start(docker_container.id, checkpoint=checkpoint_name)
        print('done')
        print(f'checkpoint {checkpoint_name} loaded')
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    prepare()
    app.run(host='0.0.0.0', port=8080)
