# GitBook Client

_A client library and CLI tool for the GitBook API_

> 📝&nbsp;&nbsp;**Note**
>
> The GitBook client is still being developed and has barely any functionality
> at the moment.

**Table of contents:**

- [Use](#use)
  - [CLI tool](#cli-tool)
- [Configure your API token](#configure-your-api-token)
- [See also](#see-also)

## Use

### CLI tool

You can invoke the CLI program with this command:

```console
$ docops-gitbook
Usage:
  docops-gitbook [options] (-h, --help)
  docops-gitbook [options] (--version)
  docops-gitbook [options] (--test-env)
  docops-gitbook [options] (--whoami)
```

Export your [API token](#configure-your-api-token):

```console
$ GITBOOK_API_TOKEN="<YOUR_TOKEN>"
$ export GITBOOK_API_TOKEN
```

Then, you can verify API authentication, like so:

```console
$ docops-gitbook --whoami
Alice Scribe (ascribe)
```

## Configure your API token

To use the GitBook client, you must have a GitBook _user_ account and a
personal GitBook _API token_. Only GitBook users may generate API tokens. You
cannot generate an API token for a GitBook _organization_.

To generate a personal API token, navigate to your GitBook profile page and
select the _Settings_ menu item. On the _Settings_ page, scroll down and select
the _API Tokens_ section, then select the _Generate new token_ button.

The _Token label_ is for your reference only. We recommend that you give it a
descriptive name like "DoiT GitBook Client". The second text box will contain
your API token string.

Before using the Python library or CLI tool, you must set the
`GITBOOK_API_TOKEN` environment variable to the value of your API token.

For example, to set the environment variable in your current shell, run
`export GITBOOK_API_TOKEN="<YOUR_TOKEN>"`, replacing `<YOUR_TOKEN>` with your
GitBook API token.

You should keep your API token a secret. The Python library and CLI tool
provide no direct way to specify an API token to reduce the chances of
accidental exposure.

## See also

- The official [GitBook developer docs][gitbook-docs]

---

🏠 [Home][home]

<!-- Link references go below this line, sorted ascending --->

[gitbook-docs]: https://developer.gitbook.com/
[home]: https://github.com/doitintl/docops-python
