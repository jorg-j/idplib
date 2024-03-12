#.ONESHELL:
#.PHONY: check_dependencies
VENV_DIR := env
VERSION := 0.0.1

clean:
	$(info ##### echo Cleaning Directories #####)
	-rm -r build
	-rm -r *.egg-info
	-rm "dist/hslib-$(VERSION)-py3-none-any.whl"

check_dependencies: $(VENV_DIR)/bin/activate
	@$(VENV_DIR)/bin/pip3 show setuptools wheel >/dev/null 2>&1 || { echo "Installing setuptools..."; $(VENV_DIR)/bin/pip3 install setuptools; }
	@$(VENV_DIR)/bin/pip3 show wheel >/dev/null 2>&1 || { echo "Installing wheel..."; $(VENV_DIR)/bin/pip3 install wheel; }

$(VENV_DIR)/bin/activate:
	python3 -m venv $(VENV_DIR)

build: clean check_dependencies
	@echo "$(VERSION)" > build_number.txt
	@$(VENV_DIR)/bin/python3 setup.py bdist_wheel


install: build
	-@$(VENV_DIR)/bin/pip3 uninstall hslib -y
	@$(VENV_DIR)/bin/pip3 install "dist/hslib-$(VERSION)-py3-none-any.whl"
