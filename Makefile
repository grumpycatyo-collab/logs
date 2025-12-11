VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: all venv install run clean activate

all: install run

venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv $(VENV); \
	else \
		echo "Virtual environment already exists"; \
	fi

install: venv
	$(PIP) install -r requirements.txt

run: venv
	$(PYTHON) bot.py

clean:
	rm -rf $(VENV)

activate: venv
	@echo "Run this command to activate the venv:"
	@echo "source $(VENV)/bin/activate"
