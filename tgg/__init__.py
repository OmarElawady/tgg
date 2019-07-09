from tgg import data
def print_default_message():
    print("""This is The Greate Gitpy. To view the help message add -h flag.""")
def execute(*args):
    print(args)
    if len(args) == 1:
        print_default_message()
    else:
        command = args[1]
        flag = ""
        passed_dict = {}
        arg_list = []
        for i in range(1, len(args)):
            if flag != "":
                passed_dict[data.params[command][flag]] = args[i]
                flag = ""
            elif args[i][0] == '-':
                flag = args[i]
            else:
                arg_list.append(args[i])
        data.functions[command](passed_dict)

