# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

# venv is a shortcut target
venv: $(VENV)/bin/activate

install:
	pip install -e .

tests:
	python3 -m pytest

run: venv
	./$(VENV)/bin/python3 src/three_spiders

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all install venv tests run clean
