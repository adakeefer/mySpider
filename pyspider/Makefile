# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	./$(VENV)/bin/python3 setup.py install

# venv is a shortcut target
venv: $(VENV)/bin/activate

tests: venv
	./$(VENV)/bin/python3 -m unittest tests.test_crawler

run: venv
	./$(VENV)/bin/python3 spider

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all venv test run clean
