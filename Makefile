#.ONESHELL:
#.PHONY: check_dependencies
.PHONY: test
VENV_DIR := env
PYTEST := $(VENV_DIR)/bin/pytest
VERSION := 0.0.1

clean:
	$(info ##### echo Cleaning Directories #####)
	-rm -r build
	-rm -r *.egg-info
	-rm "dist/IDPlib-$(VERSION)-py3-none-any.whl"

setup:
	pyenv install 3.7.16
	pyenv local 3.7.16  # Activate Python 3.7 for the current project
	poetry env use 3.7.16
	poetry install

check_dependencies:
	poetry install


build:
	poetry build


install: build
	-@$(VENV_DIR)/bin/pip3 uninstall IDPlib -y
	@$(VENV_DIR)/bin/pip3 install "dist/IDPlib-$(VERSION)-py3-none-any.whl"

test:
	poetry env use 3.7.16 && poetry run pytest tests