# language-tool-utils

At the moment, this package only contains an executable that:

* Downloads ngrams.
* Builds a Docker container using a snapshot of the https://github.com/silvio/docker-languagetool repo (which itself, downloads LanguageTool from the official page).
* Starts a server.

## Installation

https://github.com/pypa/pipx#install-pipx , then:

```
$ pipx install git+https://github.com/alexpdp7/language-tool-utils.git
```

## Usage

```
$ ltu-run-server --help
```
