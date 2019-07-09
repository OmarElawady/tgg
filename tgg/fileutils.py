import os
from distutils.dir_util import copy_tree
import shutil
import json
from random import randrange

def clear_dir(d):
    for root, dirs, files in os.walk(d):
        for f in files:
            os.remove(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def clear_dir_but_dir(d, exclude):
    for root, dirs, files in os.walk(d):
        if root == d and exclude in dirs:
            del dirs[dirs.index(exclude)]
        for f in files:
            os.remove(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def read_file(name):
    fd = open(name, 'r')
    data = fd.read()
    fd.close()
    return data
def write_to_file(name, data):
    fd = open(name, 'w+')
    fd.write(data)
    fd.close()
def read_json_file(name):
    return json.loads(read_file(name))

def write_to_json_file(name, obj):
    return write_to_file(name, json.dumps(obj))

def hash_dir(d):
    return str(randrange(100000000))

def exists(path):
    return os.path.exists(path)

def create_dir(d):
    if not exists(d):
        os.mkdir(d)

def copy_contents(source, dest):
    if not exists(dest):
        shutils.copytree(source, dest)
    else:
        for item in os.listdir(source):
            s = os.path.join(source, item)
            d = os.path.join(dest, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy(s, d)

def copy_contents_but_dir(source, dest, exclude):
    for item in os.listdir(source):
        if item == exclude:
            continue
        s = os.path.join(source, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy(s, d)
