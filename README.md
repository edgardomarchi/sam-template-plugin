# SAM Plugin Template

This is a [cookiecutter](https://github.com/audreyr/cookiecutter) template for a SAM plugin, structured as a typical Python library following modern packaging conventions . It utilizes popular libraries alongside Make and Graphviz to fully automate all development and deployment tasks.
It is based upon [Jace Browning's template](https://github.com/jacebrowning/template-python) for Python libraries.

## Features

### Development

* Preconfigured setup for [Travis CI](https://travis-ci.org/), [Coveralls](https://coveralls.io/), and [Scrutinizer](https://scrutinizer-ci.com/)
* `pyproject.toml` for managing dependencies and package metadata
* `Makefile` for automating common [development tasks](https://github.com/jacebrowning/template-python/blob/master/%7B%7Bcookiecutter.plugin_name%7D%7D/CONTRIBUTING.md):
    - Installing dependencies with `poetry`
    - Automatic formatting with `isort` and `black`
    - Static analysis with `pylint`
    - Type checking with `mypy`
    - Docstring styling with `pydocstyle`
    - Running tests with `pytest`
    - Building documentation with `mkdocs` and `pydoc-markdown` for API docs.
    - Publishing to PyPI using `poetry`

### SAM Integration

* Adecuate definition of Plugin Class
* Fully-functional UI with example elements
* Preconfigured dependencies (`sam_gui`, `plugins`)
* Ready-to-install
* Ready-to-distribute
* Basic documentation


## Usage

Install `cookiecutter` and generate a project:

```
$ pip install cookiecutter
$ cookiecutter gh:edgardomarchi/sam-template-plugin -f
```

Cookiecutter will ask you for some basic info (your name, project name, python package name, etc.) and generate a base Python project for you.

