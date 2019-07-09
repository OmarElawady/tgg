from tgg import engine

def commit(params):
    engine.VCS().add_new_commit(**params)

def init(params):
    engine.VCS().initialize()
    
def branch(params):
    engine.VCS().create_new_branch(**params)

def checkout(params):
    engine.VCS().switch_to_branch_by_name(**params)

def log(params):
    engine.VCS().log()

def revert(params):
    engine.VCS().load_commit_by_id(**params)

def merge(params):
    engine.VCS().merge_with_branch_by_name(**params)
