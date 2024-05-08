#.ONESHELL:
#.PHONY: check_dependencies
.PHONY: test enforce_version
VENV_DIR := env
PYTEST := $(VENV_DIR)/bin/pytest
VERSION := 0.0.4

# Enforce the version in the pyproject.toml
enforce_version:
	sed 's|^version = ".*|version = "$(VERSION)"|' pyproject.toml > new_toml.toml
	mv new_toml.toml pyproject.toml

clean:
	$(info ##### echo Cleaning Directories #####)
	-rm -r build
	-rm -r *.egg-info
	-rm "dist/idplib-$(VERSION)-py3-none-any.whl"

setup:
	$(info ##### setting up python 3.7.16 environment #####)
	pyenv install 3.7.16
	pyenv local 3.7.16  # Activate Python 3.7 for the current project
	poetry env use 3.7.16
	poetry install

check_dependencies:
	$(info ##### Checking Dependencies #####)
	poetry install


build: clean check_dependencies enforce_version
	$(info ##### Building Lib #####)
	poetry build

install: build
	-@$(VENV_DIR)/bin/pip3 uninstall IDPlib -y
	@$(VENV_DIR)/bin/pip3 install "dist/idplib-$(VERSION)-py3-none-any.whl"

test: build
	source $(VENV_DIR)/bin/activate && pytest tests; deactivate
	poetry env use 3.7.16 && poetry install && poetry run pytest tests

# Test using docker to ensure isolated 3.7 environment is used
ctest: build
	$(info ##### Running Docker Test #####)
	docker build -t hstest . --build-arg LIBRARYVERSION=$(VERSION)
	docker-compose up
	@docker-compose down
	@docker image rm hstest