# Python Development

> 📝 **Note**
>
> This development documentation is incomplete. More information will be added
> later.

**Table of contents:**

- [Prerequisites](#prerequisites)
- [Virtual environment](#virtual-environment)
- [Packaging](#packaging)
  - [The DoiT International namespace](#the-doit-international-namespace)

## Prerequisites

This project uses [Poetry][poetry] for packaging and dependency management. You
should have [Poetry installed][poetry-install] if you want to contribute to the
Python code in this repository.

## Virtual environment

If you have Poetry installed, you can set up your Python [virtual
environment][poetry-venv] and install the required project dependencies by
running the `poetry install` command:

<!-- TODO: Replace this with instructions that use the Makefile -->

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
`.venv` at the repository's root.

To activate the virtual environment, run the `poetry shell` command:

```console
$ poetry shell
Spawning shell within [...]/docops-python/.venv
. [...]/docops-python/.venv/bin/activate
```

After activating the virtual environment, you can import the `doitintl.docops`
Python module and run the associated CLI programs (as they exist in your local
copy of the repository).

See the [Poetry documentation][poetry-docs] for more information about how to
use the tool.

> 💡 **TIP**
>
> If you are using [Microsoft Visual Code][vscode] (VSCode), the [Python Auto
> Venv][auto-env] extension will automatically activate your Python virtual
> environment every time you open a new terminal.

<!---
TODO: Replace this next paragraph with instructions for using `make reset`
-->

If you run into a problem with your virtual environment, you can often fix it
by deleting the `.venv` directory and starting again from scratch. You can do
this using the `make reset` command at the root the repository:

```console
$ make reset
rm -rf "/workspaces/docops-python/.venv"
rm -rf "init.stamp"
```

## Packaging

### The DoiT International namespace

This project uses `doitintl` as an [implicate namespace package][pep-420].

All modules in this project are located under a namespace package directory
named `doitintl`, which must not contain an `__init__.py` file, like usual.
This method allows any other [DoiT International](https://github.com/doitintl)
projects to contribute modules to the `doitintl` namespace by following the
same pattern.

---

🏠 [Home][home]

<!-- Add link references below this line (sorted ascending) -->

[auto-env]: https://marketplace.visualstudio.com/items?itemName=whinarn.python-auto-venv
[doitintl]: https://github.com/doitintl
[pep-420]: https://www.python.org/dev/peps/pep-0420/
[poetry-docs]: https://python-poetry.org/docs/basic-usage/
[poetry-install]: https://python-poetry.org/docs/#installation
[poetry-venv]: https://python-poetry.org/docs/managing-environments/
[poetry]: https://python-poetry.org/
[vscode]: https://code.visualstudio.com/
