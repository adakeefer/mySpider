# define the name of the virtual environment directory
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

rabbitmq:
	docker run -d --hostname rabbit --name rabbit rabbitmq:3

run: venv
	./$(VENV)/bin/python3 src

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all install venv tests rabbitmq run clean
