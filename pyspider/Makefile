VENV := venv

all: venv

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

# venv is a shortcut target
venv: $(VENV)/bin/activate

install:
	pip install -e .

tests:
	./$(VENV)/bin/python3 -m pytest

cache:
	redis-stack-server --daemonize yes
	sleep 1

run: venv cache
	./$(VENV)/bin/python3 src

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	redis-cli shutdown

.PHONY: all install venv tests cache run clean
