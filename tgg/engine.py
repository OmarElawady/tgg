import os.path
import json
from tgg import fileutils
class Commit:
    def __init__(self, commit_id, parent, message = ""):
        self.commit_id = commit_id
        self.parent    = parent
        self.message   = message

    def get_id(self):
        return self.commit_id
    
    def get_parent(self):
        return self.parent
    
    def get_message(self):
        return self.message
    
    def get_json_data(self):
        obj = {}
        obj['id'] = self.get_id()
        obj['parent'] = self.parent.get_id()
        obj['message'] = self.get_message()
        return obj
    def get_path(self):
        return '.tgg/' + self.get_id()
class CommitsData:
    def __init__(self, json_data):
        self.commits = {}
        for commit in json_data:
            commit_id = commit
            parent    = json_data[commit]['parent']
            message   = json_data[commit]['message']
            self.commits[commit_id] = Commit(commit_id, parent, message)
        for commit in json_data:
            self.commits[commit].parent = self.commits[self.commits[commit].parent]
    
    def add_commit(self, commit):
        self.commits[commit.get_id()] = commit
    
    def get_json_data(self):
        obj = {}
        for commit_id in self.commits:
            commit = self.commits[commit_id]
            obj[commit.get_id()] = commit.get_json_data()
        return obj
    
    def get_commit_by_id(self, commit_id):
        return self.commits[commit_id]

    def __str__(self):
        return json.dumps(self.get_json_data(), indent = 4)

class Branch:
    def __init__(self, name, commit):
        self.commit = commit
        self.name = name

    def set_commit(self, commit):
        self.commit = commit
    
    def get_commit(self):
        return self.commit
    
    def get_name(self):
        return self.name

class BranchesData:
    def __init__(self, json_data, commits_data):
        self.branches = {}
        for branch in json_data:
            self.branches[branch] = Branch(branch, commits_data.get_commit_by_id(json_data[branch]))
    def add_branch(self, branch):
        self.branches[branch.get_name()] = branch
    
    def set_branch_commit(self, branch, commit):
        self.branches[branch.get_name()].set_commit(commit)

    def get_branch(self, branch):
        return self.branches[branch]
    def get_branch_commit(self, branch):
        return self.branches[branch].get_commit()
    def get_json_data(self):
        obj = {}
        for branch_name in self.branches:
            branch = self.branches[branch_name]
            obj[branch.get_name()] = branch.get_commit().get_id()
        return obj
    def __str__(self):
        return json.dumps(self.get_json_data(), indent = 4)

class VCS:
    def __init__(self):
        if self.is_initialized():
            self.assign_attrs()

    def assign_attrs(self):
        self.commits_data  = CommitsData(fileutils.read_json_file('.tgg/commits'))
        self.branches_data = BranchesData(fileutils.read_json_file('.tgg/branches'), self.commits_data)
        current_branch_name = fileutils.read_file('.tgg/current_branch')
        current_commit = self.branches_data.get_branch_commit(current_branch_name)
        self.current_branch = self.branches_data.get_branch(current_branch_name)
        self.current_commit = self.current_branch.get_commit()
    #------------- initialization -------------
    def initialize(self):
        if self.is_initialized():
            print("Already initialized")
            return None
        fileutils.create_dir('.tgg')
        fileutils.write_to_json_file('.tgg/commits', {"0": {"parent":"0" ,"message":""}})
        fileutils.write_to_json_file('.tgg/branches', {"master": '0'})
        fileutils.write_to_file('.tgg/current_branch', 'master') 
        self.assign_attrs()
    def is_initialized(self):
        return fileutils.exists('.tgg')
    #------------- branches -------------------
    def switch_to_branch(self, branch):
        self.current_branch = branch
    
    def switch_to_branch_by_name(self, name):
        self.switch_to_branch(self.branches_data.get_branch(name))
    
    def create_new_branch(self, name):
        self.branches_data.add_branch(Branch(name, self.current_commit))
   # TODO 
    def merge_with_branch_by_name(self, name):
        return 0

    def merge_with_branch(self, branch):
        return 0

    #------------- commits --------------------
    def load_commit(self, commit):
        self.current_commit = commit
        fileutils.clear_dir_but_dir('.', '.tgg')
        fileutils.copy_contents(self.current_commit.get_path(), '.')
   
    def load_commit_by_id(self, commit_id):
       self.load_commit(self.commits_data.get_commit_by_id(commit_id))
    
    def add_new_commit(self, message = ""):
        commit_id = fileutils.hash_dir('.')
        parent = self.current_commit
        self.current_commit = Commit(commit_id, parent, message)
        self.commits_data.add_commit(self.current_commit)
        fileutils.create_dir(self.current_commit.get_path())
        fileutils.copy_contents_but_dir('.', self.current_commit.get_path(), '.tgg')

    #------------ logging -------------------
    def print_commits_data(self):
        print(json.dumps(self.commits_data.get_json_data(), indent = 4))
        return 0

    def print_branches_data(self):
        print(json.dumps(self.branches_data.get_json_data(), indent = 4))
        return 0

    def log(self):
        print("Commits:")
        print(self.commits_data)
        print("Branches:")
        print(self.branches_data)
        print("Current branch: " + self.current_branch.get_name())
        return 0

    #---------- properties --------------
    @property
    def current_commit(self):
        return self._current_commit

    @current_commit.setter
    def current_commit(self, commit):
        self._current_commit = commit
        self.current_branch.set_commit(commit)
        self.branches_data.set_branch_commit(self.current_branch, self.current_commit)
        return 0
    
    @property
    def current_branch(self):
        return self._current_branch
    
    @current_branch.setter
    def current_branch(self, branch):
        self._current_branch = branch
    
    @property
    def branches_data(self):
        return self._branches_data
    
    @branches_data.setter
    def branches_data(self, data):
        self._branches_data = data

    @property
    def commits_data(self):
        return self._commits_data
    
    @commits_data.setter
    def commits_data(self, data):
        self._commits_data = data
    
    #--------------- destructor ----------------
    def __del__(self):
        fileutils.write_to_json_file('.tgg/commits', self.commits_data.get_json_data())
        fileutils.write_to_json_file('.tgg/branches', self.branches_data.get_json_data())
        fileutils.write_to_file('.tgg/current_branch', self.current_branch.get_name())
