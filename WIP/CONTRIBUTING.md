# Contributing

Table of contents:

- [Python](#python)
  - [Create a local virtual environment](#create-a-local-virtual-environment)
  - [Prepare a new release](#prepare-a-new-release)
  - [Publish to PyPI](#publish-to-pypi)

## Python development

### Create a local virtual environment

This project uses [Poetry](https://python-poetry.org/) for packaging and
dependency management. You must [install
Poetry](https://python-poetry.org/docs/#installation) before continuing.

If you have Poetry installed, you can set up a local Python [virtual
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
Spawning shell within [...]/.venv
. [...]/.venv/bin/activate
```

After you have activated the virtual environment, you can run any of the
configured CLI entry points (as they exist in your local copy of the
repository).

Consult the [Poetry documentation](https://python-poetry.org/docs/basic-usage/)
for more information.

> :point_up: **TIP**: If you are using [Microsoft Visual
> Code](https://code.visualstudio.com/) (VSCode), you must select the Python
> interpreter inside the project `.venv` directory for most Python-related
> features to work correctly. Additionally, VSCode will automatically activate
> your virtual environment every time you open a new terminal.

If you run into a problem with your virtual environment, you can often fix it
by deleting the `.venv` directory and starting again from scratch. Run `make
reset` to delete your virtual environment.

### Prepare a new release

> :construction: **TODO: Should probably automate this whole thing with a shell script,
> including git commands, checks for updates to the changelog, etc**

> :construction: **TODO: Mention how to [configure
> Poetry](https://python-poetry.org/docs/repositories/#configuring-credentials)
> securly for publishing Python packages**
