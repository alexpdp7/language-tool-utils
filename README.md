# language-tool-utils

At the moment, this project contains executables that:

* Downloads ngrams, builds a Docker container using a snapshot of the https://github.com/silvio/docker-languagetool repo (which itself, downloads LanguageTool from the official page), and starts a server
* Generates an HTML file from an AsciiDoctor file and checks it using the LanguageTool HTTP API (skipping code blocks, etc.)

, and some Python libraries to help implement that.

## Installation

https://github.com/pypa/pipx#install-pipx , then:

```
$ pipx install git+https://github.com/alexpdp7/language-tool-utils.git
```

## Usage

```
$ ltu-build-server --ngrams en
$ ltu-run-server
# switch to a different tab
$ ltu-check-asciidoctor --language en path-to-asciidoc.adoc
```

Review the `--help` option in some commands for details.
