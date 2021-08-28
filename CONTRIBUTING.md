# Contributing

Table of contents:

- [Contributing](#contributing)
  - [Python](#python)
    - [Virtual environment](#virtual-environment)

## Python

### Virtual environment

This project uses [Poetry](https://python-poetry.org/) for packaging and
dependency management. You must [install
Poetry](https://python-poetry.org/docs/#installation) before continuing.

If you have Poetry installed, you can set up your Python [virtual
environment](https://python-poetry.org/docs/managing-environments/) and install
the required project dependencies by running the `poetry install` command:

```console
$ poetry install
Installing dependencies from lock file

Package operations: [...] installs, 0 updates, 0 removals

  • Installing [...]  ([...])
  • Installing [...]  ([...])
  • Installing [...]  ([...])
[...]
```

This command will create a Python virtual environment in a directory named
`.venv` at the root of the repository.

To activate the virtual environment, run the `poetry shell` command:

```console
$ poetry shell
Spawning shell within [...]/gbclient/.venv
. [...]/gbclient/.venv/bin/activate
```

After you have activated the virtual environment, you can run the `gbclient`
program and import the `gbclient` Python library (as they exist in your local
copy of the repository).

Consult the [Poetry documentation](https://python-poetry.org/docs/basic-usage/)
for more information.

> **TIP**: If you are using [Microsoft Visual
> Code](https://code.visualstudio.com/) (VSCode), you must select the Python
> interpreter inside the project `.venv` directory for most Python-related
> features to work correctly. Additionally, VSCode will automatically activate
> your virtual environment every time you open a new terminal.

If you run into a problem with your virtual environment, you can often fix it
by deleting the `.venv` directory and starting again from scratch.
