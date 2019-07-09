import os.path
import json
from tgg import fileutils
class Commit:
    def __init__(self, commit_id, parent, message = ""):
        self.commit_id = commit_id
        self.parent    = parent
        self.message   = message
        return 0

    def get_id(self):
        return self.commit_id
    
    def get_parent(self):
        return self.parent
    
    def get_message(self):
        return self.message
    
    def get_json_data(self):
        return {'id': self.get_id(), 'parent': self.parent.get_id(), 'message': self.get_message()}

class CommitsData:
    def __init__(self, json_data):
        self.commits = {}
        for commit in json_data:
            commit_id = commit
            parent    = json_data[commit]['parent']
            message   = json_data[commit]['message']
            self.commits[commit_id] = Commit(commid_id, parent, message)
    
    def add_commit(self, commit):
        self.commits[commits.get_id()] = commit
    
    def get_json_data(self, commit):
        obj = {}
        for commit in self.commits:
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
        self.branches[branch.get_name()] = commit.get_id()

    def get_branch(self, branch):
        return self.branches[branch]

    def get_json_data(self):
        obj = {}
        for branch in self.branches:
            obj[branch.get_name()] = branch.get_commit().get_id()
        return obj
    def __str__(self):
        return json.dumps(self.get_json_data(), indent = 4)

class VCS:
    def __init__(self):
        if self.is_initialized():
            self.commits_data  = BranchesData(fileutils.read_json_file('.tgg/commits'))
            self.branches_data = BranchesData(fileutils.read_json_file('.tgg/branches'))
            current_branch_name = Branch(fileutils.read_file('.tgg/current_branch'))
            current_commit = self.branches_data.get_branch_commit(current_branch_name)
            self.current_branch = self.branches_data.get_branch(current_branch_name)
            self.current_commit = self.current_branch.get_commit()
        return 0

    #------------- initialization -------------
    def initialize(self):
        fileutils.create_dir('.tgg')
    def is_initialized(self):
        return fileutils.exists('.tgg')
    #------------- beanches -------------------
    def switch_to_branch(self, branch):
        self.current_branch = branch
    
    def switch_to_branch_by_name(self, name):
        switch_to_branch()
    
    def create_new_branch(self, branch):
        self.branches_data.adBranch(self.current_commit)
    
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
        commit_id = fileutils.hash_dir(d)
        parent = self.current_commit
        self.current_commit = Commit(commit_id, parent, message)
        self.commits_data.add_commit()
        filutils.create_dir(self.current_commit.get_path())
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
        print("Current branch" + self.current_branch.get_name())
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
        self.current_branch = branch
    
    @property
    def branches_data(self):
        return self._branches_data
    
    @branches_data.setter
    def branches_data(self, data):
        self._branches_data = data

    @property
    def commits_data(self):
        self._commits_data = data
    
    @commits_data.setter
    def commits_data(self, data):
        self._commits_data = data
    
    #--------------- destructor ----------------
    def __del__(self):
        fileutils.write_to_json_file('.tgg/commits', self.commits_data.get_json_data())
        fileutils.write_to_json_file('.tgg/branches', self.branches_data.get_json_data())
        fileutils.write_to_file('.tgg/current_branch', self.current_branch.get_name())
