# Overview

{{cookiecutter.project_short_description}}

This project was generated with [cookiecutter](https://github.com/audreyr/cookiecutter) using a template based on [jacebrowning/template-python](https://github.com/jacebrowning/template-python).

[![Unix Build Status](https://img.shields.io/travis/{{cookiecutter.github_username}}/{{cookiecutter.github_repo}}/{{cookiecutter.default_branch}}.svg?label=unix)](https://travis-ci.org/{{cookiecutter.github_username}}/{{cookiecutter.github_repo}})
[![Windows Build Status](https://img.shields.io/appveyor/ci/{{cookiecutter.github_username}}/{{cookiecutter.github_repo}}/{{cookiecutter.default_branch}}.svg?label=window)](https://ci.appveyor.com/project/{{cookiecutter.github_username}}/{{cookiecutter.github_repo}})
[![Coverage Status](https://img.shields.io/coveralls/{{cookiecutter.github_username}}/{{cookiecutter.github_repo}}/{{cookiecutter.default_branch}}.svg)](https://coveralls.io/r/{{cookiecutter.github_username}}/{{cookiecutter.github_repo}})
[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/{{cookiecutter.github_username}}/{{cookiecutter.github_repo}}.svg)](https://scrutinizer-ci.com/g/{{cookiecutter.github_username}}/{{cookiecutter.github_repo}}/?branch={{cookiecutter.default_branch}})
[![PyPI Version](https://img.shields.io/pypi/v/{{cookiecutter.plugin_name}}.svg)](https://pypi.org/project/{{cookiecutter.plugin_name}})
[![PyPI License](https://img.shields.io/pypi/l/{{cookiecutter.plugin_name}}.svg)](https://pypi.org/project/{{cookiecutter.plugin_name}})

# Setup

## Requirements

* Python {{cookiecutter.python_major_version}}.{{cookiecutter.python_minor_version}}+
* Plugins package

## Installation

Install this library directly into an activated virtual environment:

```text
$ pip install {{cookiecutter.plugin_name}}
```

or add it to your [Poetry](https://poetry.eustace.io/) project:

```text
$ poetry add {{cookiecutter.plugin_name}}
```

# Usage

After installation, the package can imported:

```text
$ python
>>> import {{cookiecutter.plugin_name}}
>>> {{cookiecutter.plugin_name}}.__version__
```
For using it within a host application, plugin must be registered first with the ```plugins``` package:

```
$ plugins register {{cookiecutter.plugin_name}}
```
