TGG
===
This is a git-like package.

Usage
=====

Initializing a tgg repo:

```tgg init```

View commits and branches and current branch:

```tgg log```

Make a commit to the current branch:

```tgg commit -m "message"```

Create a new branch:

```tgg branch -b name```

Checkout to another branch:

```tgg checkout -b name```

Restore a commit:

```tgg revert -c commit_id```

Track a file:

```tgg track file_name```

Untrack a file:

```tgg untrack file_name```

Installation
============

It can be installed in a pip virtual environment using the command:

```pipenv -e .```

After that, it can be used by executing ```pipenv shell``` and running tgg commands.
