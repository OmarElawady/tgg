from tgg import engine
import click

@click.group()
def main():
    pass

@click.command()
@click.option('-m', default="", help="The message associated with the commit")
def commit(m):
    e = engine.VCS()
    if not e.is_initialized():
        print("No tgg repo found")
        return
    e.add_new_commit(m)

@click.command()
def init():
    engine.VCS().initialize()
    
@click.command()
@click.option('-b', help="The name of the created branch")
def branch(b):
    e = engine.VCS()
    if not e.is_initialized():
        print("No tgg repo found")
        return
    e.create_new_branch(b)


@click.command()
@click.option('-b', help="The name of the branch to switch to")
def checkout():
    e = engine.VCS()
    if not e.is_initialized():
        print("No tgg repo found")
        return
    e.switch_to_branch_by_name(b)

@click.command()
def log():
    e = engine.VCS()
    if not e.is_initialized():
        print("No tgg repo found")
        return
    e.log()

@click.command()
@click.option('-c', help="The id of the commit")
def revert(c):
    e = engine.VCS()
    if not e.is_initialized():
        print("No tgg repo found")
        return
    e.load_commit_by_id(c)

@click.command()
@click.option('-b', help="The branch name(to be implemented)")
def merge(b):
    e = engine.VCS()
    if not e.is_initialized():
        print("No tgg repo found")
        return
    e.merge_with_branch_by_name(b)

@click.command()
def status():
    e = engine.VCS()
    if not e.is_initialized():
        print("No tgg repo found")
        return
    e.view_status()
@click.command()
@click.argument('name')
def add(name):
    e = engine.VCS()
    if not e.is_initialized():
        print("No tgg repo found")
        return
    e.track_file(name)
main.add_command(init)
main.add_command(commit)
main.add_command(merge)
main.add_command(revert)
main.add_command(branch)
main.add_command(checkout)
main.add_command(log)
main.add_command(status)
main.add_command(add)
