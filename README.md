# DocOps at DoiT

_Common resources to help with doing DocOps at DoiT International_

[![CICD][cicd-badge]][cicd-workflow] [![CodeQL][codeql-badge]][codeql-workflow]

[cicd-badge]: https://github.com/doitintl/docops/actions/workflows/cicd.yaml/badge.svg
[cicd-workflow]: https://github.com/doitintl/docops/actions/workflows/cicd.yml
[codeql-badge]: https://github.com/doitintl/docops/actions/workflows/codeql.yml/badge.svg
[codeql-workflow]: https://github.com/doitintl/docops/actions/workflows/codeql.yml

**Table of contents**

- [Development containers](#development-containers)
  - [Remote development](#remote-development)
  - [Local development](#local-development)

## Development containers

You can use [development containers][devcontainers] (devcontainers) to work on GitHub repositories entirely within a Docker container.

This repository provides a [DocOps devcontainer][devcontainer] image that includes all of the software you will need for working on the DoiT International [docops][docops] and [docs][docs] repositories.

We designed the DocOps devcontainer image for dual use with Microsoft [Visual Studio Code][vscode] (VS Code) and [GitHub Actions][gh-actions]. The image uses the latest VS Code [Debian devcontainer][vscode-images] image as a base.

[GitHub Codespaces][codespaces] allows you to run devcontainers remotely. However, you can also run devcontainers locally with the [VS Code Remote - Containers extension][remote-containers].

> **Tip**
>
> Because devcontainers are regular Docker containers, you are not required to use them with GitHub Codespaces or VS Code. If you have an alternative setup that works for you, please share it with others by contributing to this document.

### Remote development

GitHub Codespaces allows you to work on repositories inside a devcontainer that runs remotely on GitHub's cloud infrastructure.

The DoiT International [docops][docops] and [docs][docs] repositories are pre-configured to use the [DocOps devcontainer][devcontainer].

If you're a member of the [DoiT GitHub organization][doit-gh] and have access to the GitHub Codespaces feature, select the _Code_ drop-down menu from a repository homepage, then select _New codespace_ from the _Codespaces_ tab to launch a new codespace.

When you select _New codespace_, GitHub will present you with the option to use your codespace with the [GitHub web-based editor][gh-editor] ([VS Code for the Web][vscode-web]) or the desktop version of VS Code (with the [GitHub Codespaces extension][codespaces-ext])

> **See also**
>
> - [GitHub Docs: GitHub Codespaces overview][codespaces-docs]

### Local development

If you have [Docker Desktop][docker-desktop] installed, you can pull the DocOps devcontainer image and run it locally.

First, create a new [personal authentication token][pat] (PAT) and export it to your environment:

```console
$ export CR_PAT=YOUR_TOKEN
```

Then, use your PAT to [authenticate][containers-auth] with the [GitHub Container registry][gh-containers]:

```console
$ echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
Login Succeeded
```

Finally, pull the [devcontainer][devcontainer] image:

```console
$ docker pull ghcr.io/doitintl/docops/devcontainer:main
main: Pulling from doitintl/docops/devcontainer
0c6b8ff8c37e: Pull complete
412caad352a3: Pull complete
e6d3e61f7a50: Pull complete
f458a448b74e: Pull complete
84c3ca02abb3: Pull complete
b592074de274: Pull complete
4f4fb700ef54: Pull complete
caf0431a02d9: Pull complete
Digest: sha256:a3d95d52706b1936ebeb014d3f952cce97e8339055e5cec04e76602e1b444383
Status: Downloaded newer image for ghcr.io/doitintl/docops/devcontainer:main
ghcr.io/doitintl/docops/devcontainer:main
```

As long as you remain authenticated with the registry, you can use the [VS Code Remote - Containers extension][remote-containers] to clone any GitHub repository into a running version of the DocOps devcontainer.

To do this, within VS Code, run one of the available _Remote-Containers: Clone Repository in&hellip;_ commands and enter the repository URL when prompted. Because the DoiT International [docops][docops] and [docs][docs] repositories are pre-configured to use the DocOps devcontainer, VS Code will start the devcontainer for these repositories without any additional prompts.


[pat]: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
[containers-auth]: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-to-the-container-registry
[gh-containers]: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry
[docker-desktop]: https://www.docker.com/products/docker-desktop
[codespaces-ext]: https://marketplace.visualstudio.com/items?itemName=GitHub.codespaces
[vscode-web]: https://code.visualstudio.com/docs/editor/vscode-web
[gh-editor]: https://docs.github.com/en/codespaces/the-githubdev-web-based-editor
[doit-gh]: https://github.com/doitintl
[codespaces-docs]: https://docs.github.com/en/codespaces/overview
[codespaces]: https://github.com/features/codespaces
[devcontainer]: https://github.com/doitintl/docops/pkgs/container/docops%2Fdevcontainer
[docops]: https://github.com/doitintl/docops
[docs]: https://github.com/doitintl/docs
[vscode]: https://code.visualstudio.com/
[gh-actions]: https://github.com/features/actions
[vscode-images]: https://hub.docker.com/_/microsoft-vscode-devcontainers
[devcontainers]: https://code.visualstudio.com/docs/remote/containers
[remote-containers]: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers
