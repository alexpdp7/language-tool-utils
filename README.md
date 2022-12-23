# language-tool-utils

At the moment, this package executables that:

* Downloads ngrams, builds a Docker container using a snapshot of the https://github.com/silvio/docker-languagetool repo (which itself, downloads LanguageTool from the official page), and starts a server
* Generates an HTML file from an AsciiDoctor file and checks it using the LanguageTool HTTP API (skipping code blocks, etc.)

## Installation

https://github.com/pypa/pipx#install-pipx , then:

```
$ pipx install git+https://github.com/alexpdp7/language-tool-utils.git
```

## Usage

```
$ ltu-run-server --help
$ ltu-check-asciidoctor --help
```
