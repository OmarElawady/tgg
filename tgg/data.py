from tgg import funcs

commands = {
    "commit"
    , "init"
    , "checkout"
    , "branch"
    , "log"
    , "revert"
    , "merge"
}
params = {
    "commit":{
        "-m": "message"
    }
    , "init": {}
    , "checkout": {
        "-b": "name"  
    }
    , "branch": {
        "-b": "name"    
    }
    , "log": {}
    , "revert": {
        "-c": "commit_id"    
    }
    , "merge": {
        "-b": "name"
    }
}
params_count = {
    "commit":{
        "message": 1
    }
    , "init": {}
    , "checkout": {
        "branch": 1    
    }
    , "branch": {
        "branch": 1    
    }
    , "log": {}
    , "revert": {
        "commit": 1
    }
    , "merge":{
        "branch": 1
    }
}
functions = {
        "commit": funcs.commit
        , "init": funcs.init
        , "checkout": funcs.checkout
        , "branch": funcs.branch
        , "log": funcs.log
        , "revert": funcs.revert
        , "merge": funcs.merge
}
