import os.path
import json
import shutil
from distutils.dir_util import copy_tree

def initialize():
    if os.path.exists(".tgg"):
        print("Already initialized")
        return None
    os.mkdir(".tgg")
    put_branches_data({"master": "0"})
    switch_to_branch("master")
    put_commit_data({})

def initialized():
    return os.path.exists(".tgg")

def get_current_branch():
    return open(".tgg/current_branch", "r").read()

def get_current_commit():
    return get_branch_commit(get_current_branch())

def parse_json_file(name):
    fd = open(name, "r")
    return json.loads(fd.read())

def get_branches_data():
    branches_data = parse_json_file(".tgg/branches")
    return branches_data

def put_branches_data(data):
    fd = open(".tgg/branches", "w")
    fd.write(json.dumps(data))

def get_branch_commit(branch):
    print(branch)
    return get_branches_data()[branch]

def add_branch(branch):
    branches_data = parse_json_file(".tgg/branches")
    branches_data[branch] = get_current_commit()
    put_branches_data(branches_data)

def switch_to_branch(branch):
    fd = open(".tgg/current_branch", "w")
    fd.write(branch)
def set_branch_commit(branch, commit):
    data = get_branches_data()
    data[branch] = commit
    put_branches_data(data)

def get_commit_data():
    return parse_json_file(".tgg/commits")

def put_commit_data(data):
    fd = open(".tgg/commits", "w")
    fd.write(json.dumps(data))


def commit_message(commit):
    return get_commit_data()[commit]["message"]

def commit_parent(commit):
    return get_commit_data()[commit]["parent"]

def save_working_directory(commit_id):
    clear_temp() 
    os.mkdir(".tgg/" + commit_id)
    os.mkdir('/tmp/tgg.tmp')
    copy_tree(".", "/tmp/tgg.tmp")
    
    copy_tree("/tmp/tgg.tmp", ".tgg/" + commit_id)
    shutil.rmtree(".tgg/" + commit_id + "/.tgg")

def load_commit_directory(commit_id):
    os.mkdir("/temp/tgg.tmp")
    copy_tree(".tgg/", "/temp/tgg.tmp")
    import shutil
    shutil.rmtree(".")
    copy_tree("/temp/tgg.tmp/" + commit_id, '.')
    os.mkdir(".tgg")
    copy_tree("/temp/tgg.tmp/.tgg", ".tgg")
    
def get_hash_of_dir(directory, verbose=0):
    import hashlib, os
    SHAhash = hashlib.md5()
    if not os.path.exists (directory):
        return -1

    try:
        for root, dirs, files in os.walk(directory):
            for names in files:
                filepath = os.path.join(root,names)
                try:
                    f1 = open(filepath, 'r', encoding = "utf-8")
                    
                except:
                    # You can't open the file for some reason
                    continue
                while 1:
                    # Read file in as little chunks
               
                    buf = f1.read(4096)
                    if not buf : break
                    SHAhash.update(hashlib.md5(buf.encode('utf-8')).hexdigest().encode('utf-8'))
                f1.close()
    except:
        import traceback
        # Print the stack traceback
        traceback.print_exc()
        return -2
    from random import randrange
    SHAhash.update(hashlib.md5(str(randrange(0, 10000000)).encode('utf-8')).hexdigest().encode('utf-8'))
    return SHAhash.hexdigest()   

def new_commit_data(commit_id, message):
    d = {}
    d["id"] = commit_id
    d["message"] = message
    d["parent"] = get_current_commit()
    return d

def add_commit(message = ""):
    commits = get_commit_data()
    commit_id = get_hash_of_dir(".")
    commits[commit_id] = new_commit_data(commit_id, message)
    save_working_directory(commit_id)
    put_commit_data(commits)
    set_branch_commit(get_current_branch(), commit_id)

def clear_dir():
    for root, dirs, files in os.walk('.'):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
def clear_but_tgg():
    clear_temp()
    copy_tree('.tgg', '/tmp/tgg.tmp')
    clear_dir()
    copy_tree("/tmp/tgg.tmp", ".tgg")


def clear_temp():
    if os.path.exists('/tmp/tgg.tmp'):
        shutil.rmtree('/tmp/tgg.tmp')

def load_commit(commit):
    clear_temp()
    copy_tree('.', '/tmp/tgg.tmp')
    clear_dir()
    copy_tree('/tmp/tgg.tmp/.tgg/' + commit, '.')
    copy_tree('/tmp/tgg.tmp/.tgg/', '.tgg')
    set_branch_commit(get_current_branch(), commit)

def print_commit_data():
    print(json.dumps(get_commit_data(), indent=4))

def print_branch_data():
    print(json.dumps(get_branches_data(), indent=4))

def print_data():
    print("Commits:")
    print_commit_data()
    print("Branches:")
    print_branch_data()
    print("Current branch:" + get_current_branch())
# create new branch and switch to it
def create_new_branch(branch):
    obj = get_branches_data()
    obj[branch] = get_current_commit()
    put_branches_data(obj)
    switch_to_branch(branch)

# merge the current branch to another branch
def merge_with_branch(branch):
    commit1 = get_branch_commit(branch)
    commit2 = get_branch_commit(get_current_branch())
    clear_but_tgg()
    copy_tree('.tgg/' + commit1, '.')
    copy_tree('.tgg/' + commit2, '.')
    import ipdb;ipdb.set_trace()
    add_commit('merged ' + commit1 + " with " + commit2)
