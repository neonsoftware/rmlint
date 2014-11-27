#############
# UTILITIES #
#############

import subprocess
import shutil
import json
import os


TESTDIR_NAME = '/tmp/rmlint-unit-testdir'

def runs_as_root():
    return os.geteuid() is 0


def create_testdir():
    try:
        os.makedirs(TESTDIR_NAME)
    except OSError:
        pass


def run_rmlint(*args, dir_suffix=None, use_default_dir=True):
    if use_default_dir:
        if dir_suffix:
            target_dir = os.path.join(TESTDIR_NAME, dir_suffix)
        else:
            target_dir = TESTDIR_NAME
    else:
        target_dir = ""

    cmd = ' '.join(['./rmlint', target_dir, '-o json:stdout'] + list(args))
    output = subprocess.check_output(cmd, shell=True)
    json_data = output.decode('utf-8')
    return json.loads(json_data)


def create_dirs(path):
    os.makedirs(os.path.join(TESTDIR_NAME, path))


def create_link(path, target, symlink=False):
    f = os.symlink if symlink else os.link
    f(
        os.path.join(TESTDIR_NAME, path),
        os.path.join(TESTDIR_NAME, target)
    )


def create_file(data, name):
    full_path = os.path.join(TESTDIR_NAME, name)
    if '/' in name:
        try:
            os.makedirs(os.path.dirname(full_path))
        except OSError:
            pass

    with open(full_path, 'w') as handle:
        handle.write(data)


def usual_setup_func():
    create_testdir()


def usual_teardown_func():
    shutil.rmtree(TESTDIR_NAME)