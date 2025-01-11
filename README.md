# python project template

Template poetry + devcontainer project.

# To use

1. Clone
2. Rename project folder from python-template to name of project
3. delete .git
4. git init
5. Follow either with/without devcontainer...

## With devctonainer

1. Rename pyproject.toml name to name of project
2. Rename .devcontainer/devcontainer.json name to name of project
3. Rename .devcontainer/Dockerfile.dev PROEJCT_NAME to name of project
4. Run devcontainer

## Without devcontainer

1. Rename pyproject.toml name to name of project
2. sudo apt install pipx
3. pipx install poetry
4. poetry shell
5. poetry install

## Pre-commit

1. Edit `.pre-commit-config.yaml` and uncomment the block on no commit main
2. Run `pre-commit install`

# Useful additions 

## Notebook stripout pre-commit 

A hook to remove outputs from notebooks for all commits. This cuts bloat from git history.

## Packaged core

Poetry packages core, so notebooks can access without any path appends. 

## Test notebooks runnable with papermill

`python3 core/utils/check_notebooks.py` will use papermill to run all notebooks in project. This is useful to check none are out of date.
