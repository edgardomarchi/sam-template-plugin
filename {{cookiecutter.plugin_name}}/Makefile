# Project settings
PACKAGE := $(firstword $(shell poetry version))
PROJECT := $(PACKAGE)
REPOSITORY := http://dilbert.inti.gob.ar/gitlab/auto/{{cookiecutter.github_repo}}
VERSION = $(word 2,$(shell poetry version))

# Project paths
CONFIG := $(wildcard *.py)
MODULES := $(wildcard $(PACKAGE)/*.py)

# Virtual environment paths
VIRTUAL_ENV := .venv

# ARG processing
DEFAULTARG=patch

# aux functions
include makeutils/functions.mk

# commands
BUMPVERSION = bump2version

# MAIN TASKS ##################################################################

.DEFAULT: ;

.PHONY: all
all: install

.PHONY: ci
ci: format check test mkdocs ## Run all tasks that determine CI status

.PHONY: watch
watch: install .clean-test ## Continuously run all CI tasks when files chanage
	poetry run sniffer

.PHONY: run ## Start the program
run: install
	poetry run python $(PACKAGE)/__main__.py

# SYSTEM DEPENDENCIES #########################################################

.PHONY: doctor
doctor:  ## Confirm system dependencies are available
	bin/verchew

# PROJECT DEPENDENCIES ########################################################

DEPENDENCIES := $(VIRTUAL_ENV)/.poetry-$(shell bin/checksum pyproject.toml poetry.lock)

.PHONY: install
install: $(DEPENDENCIES) .cache
	@if ! $(call check-package,$(PACKAGE)) ; then      \
	  echo "$(PACKAGE) not installed. Installing ..." ;\
	  poetry install                                  ;\
	fi

$(DEPENDENCIES): poetry.lock
	@ poetry config virtualenvs.in-project true
	poetry install --no-root
	@ touch $@

poetry.lock: pyproject.toml
	poetry lock
	@ touch $@

.cache:
	@ mkdir -p .cache

# CHECKS ######################################################################

.PHONY: format
format: install
	poetry run isort $(PACKAGE) --recursive --apply
	poetry run black $(PACKAGE)
	@ echo

.PHONY: check
check: install format  ## Run formaters, linters, and static analysis
ifdef CI
	git diff --exit-code
endif
	poetry run pylint $(PACKAGE) --rcfile=.pylint.ini
	poetry run mypy $(PACKAGE) --config-file=.mypy.ini
	poetry run pydocstyle $(PACKAGE) $(CONFIG)

# TESTS #######################################################################

RANDOM_SEED ?= $(shell date +%s)
FAILURES := .cache/v/cache/lastfailed

PYTEST_OPTIONS := --random --random-seed=$(RANDOM_SEED)
ifdef DISABLE_COVERAGE
PYTEST_OPTIONS += --no-cov --disable-warnings
endif
PYTEST_RERUN_OPTIONS := --last-failed --exitfirst

.PHONY: test
test: test-all ## Run unit and integration tests

.PHONY: test-unit
test-unit: install
	@ ( mv $(FAILURES) $(FAILURES).bak || true ) > /dev/null 2>&1
	poetry run pytest $(PACKAGE) $(PYTEST_OPTIONS)
	@ ( mv $(FAILURES).bak $(FAILURES) || true ) > /dev/null 2>&1
	poetry run coveragespace $(REPOSITORY) unit

.PHONY: test-int
test-int: install
	@ if test -e $(FAILURES); then poetry run pytest tests $(PYTEST_RERUN_OPTIONS); fi
	@ rm -rf $(FAILURES)
	poetry run pytest tests $(PYTEST_OPTIONS)
	poetry run coveragespace $(REPOSITORY) integration

.PHONY: test-all
test-all: install
	@ if test -e $(FAILURES); then poetry run pytest $(PACKAGE) $(PYTEST_RERUN_OPTIONS); fi
	@ rm -rf $(FAILURES)
	poetry run pytest tests $(PACKAGE) $(PYTEST_OPTIONS)
	poetry run coveragespace $(REPOSITORY) overall

.PHONY: read-coverage
read-coverage:
	bin/open htmlcov/index.html

# DOCUMENTATION ###############################################################

SPHINX_INDEX := docs/_build/index.html

.PHONY: docs
docs: sphinx uml ## Generate documentation and UML

.PHONY: sphinx
sphinx: install $(SPHINX_INDEX)

$(SPHINX_INDEX): docs/*.md
	@ mkdir -p docs/about
	@ cd docs && ln -sf ../README.md README.md
	@ cd docs/about && ln -sf ../../CHANGELOG.md changelog.md
	@ cd docs/about && ln -sf ../../CONTRIBUTING.md contributing.md
	@ cd docs/about && ln -sf ../../LICENSE.md license.md
	cd docs && $(MAKE) clean
	cd docs && $(MAKE) html

.PHONY: uml
uml: install docs/*.png
docs/*.png: $(MODULES)
	poetry run pyreverse $(PACKAGE) -p $(PACKAGE) -a 1 -f ALL -o png --ignore tests
	- mv -f classes_$(PACKAGE).png docs/classes.png
	- mv -f packages_$(PACKAGE).png docs/packages.png

# .PHONY: sphinx-serve
# sphinx-serve: sphinx
# 	python -m http.server http://localhost:8000/build_/html/index.html



# BUILD #######################################################################

EXE_FILES := dist/$(PACKAGE).*

SDIST := dist/$(PACKAGE)-$(VERSION)*.tar.gz
WHEEL := dist/$(PACKAGE)-$(VERSION)*.whl

DIST_FILES := $(SDIST) $(WHEEL)

.PHONY: dist
dist: install $(DIST_FILES)

$(SDIST): $(MODULES) pyproject.toml
	@ poetry build -f sdist

$(WHEEL): $(MODULES) pyproject.toml
	@ poetry build -f wheel

# For framework/shared support: https://github.com/yyuu/pyenv/wiki
.PHONY: exe
exe: install $(EXE_FILES)
$(EXE_FILES): $(MODULES) $(PACKAGE).spec
	poetry run pyinstaller $(PACKAGE).spec --noconfirm --clean

$(PACKAGE).spec:
	poetry run pyi-makespec $(PACKAGE)/__main__.py --onefile --windowed --name=$(PACKAGE)

# RELEASE #####################################################################

.PHONY: version version-chk
version-chk: install
	@$(call check-create-branch,master)
	@$(call check-create-branch,develop)
	@$(call assert-command-present,$(BUMPVERSION))
	@$(check-wd)
	@ echo "Checking out develop ..." && git checkout develop --quiet
	@ echo "Commiting 'poetry.lock' if required ..."
	@ git add poetry.lock
	@ git commit --porcelain -m"poetry.lock" || true
	@$(call check-upstream,master)
	@$(call check-upstream,develop)

version: version-chk ## Make a version bumps and push it to master
	@ echo "Checking out master ..." && git checkout master --quiet
	@ echo "Merging develop into master" && \
	  git merge -m"Merge branch 'develop'" --quiet --no-ff develop
	@ poetry run $(BUMPVERSION) $(FIRSTARG)
	@ git push --set-upstream origin master
	@ git push origin --tags
	@ echo "Checking out develop ..." && git checkout develop
	@ git merge -m"Merge branch 'master' into 'develop'" --quiet --no-ff master
	@ git push --set-upstream origin develop
	@ git push origin --tags
	@ $(call inf,version dump: $(VERSION) OK!)

.PHONY: upload
upload: version dist ## Upload the current version to pypiserver(dilbert)
	@ poetry publish -r dilbert
	@ bin/open http://dilbert.inti.gob.ar/pypiserver/simple/$(PACKAGE)


# CLEANUP #####################################################################

.PHONY: clean
clean: .clean-build .clean-docs .clean-test .clean-install ## Delete all generated and temporary files

.PHONY: clean-all
clean-all: clean
	rm -rf $(VIRTUAL_ENV)

.PHONY: .clean-install
.clean-install:
	find $(PACKAGE) -path '*/__pycache__*' -delete
	find $(PACKAGE) -type d -name '__pycache__' -empty -delete
	rm -rf *.egg-info

.PHONY: .clean-test
.clean-test:
	rm -rf .cache .pytest .coverage htmlcov

.PHONY: .clean-docs
.clean-docs:
	rm -rf docs/*.png site

.PHONY: .clean-build
.clean-build:
	rm -rf *.spec dist build

# HELP ########################################################################
.PHONY: help
help: all
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
