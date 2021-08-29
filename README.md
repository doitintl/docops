# GitBook API Python Client

Unofficial Python client library and CLI tool for the GitBook API.

This project is still being developed and has no functionality at the moment.

## Install

The GitBook API Python Client has not yet been published to the Python Package
Index (PyPI), so if you wish to install it, you must [do so
manually](CONTRIBUTING.md).

After installation, you will be able to:

- Import the `gitbook` Python client library
- Run the `gbc` CLI tool

## Configure your API token

To use this software, you must have a GitBook *user* account and a personal
GitBook *API token*. Only GitBook users may generate API tokens. You cannot
generate an API token for a GitBook *organization*.

To generate a personal API token, navigate to your GitBook profile page and
select the *Settings* menu item. On the *Settings* page, scroll down and select
the *API Tokens* section, then select the *Generate new token* button.

The *Token label* is for your reference only. We recommend that you give it a
descriptive name like "GitBook API Python Client". The second text box will
contain your API token string.

Before using the Python library or CLI tool, you must set the
`GITBOOK_API_TOKEN` environment variable to the value of your API token.

For example, to set the environment variable in your current shell, run `export
GITBOOK_API_TOKEN="<YOUR_TOKEN>"`, replacing `<YOUR_TOKEN>` with your GitBook
API token.

You should keep your API token a secret. To reduce the chances of accidental
exposure, the Python library and CLI tool provide no direct way to specify an
API token.

## Contributing

This project is maintained by [DoiT
International](https://github.com/doitintl), but we welcome community
contributions!

See the [contribution docs](CONTRIBUTING.md) for more information.

## See also

- The official [GitBook developer docs](https://developer.gitbook.com/)
