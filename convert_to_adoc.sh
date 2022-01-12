cd $(dirname $0)
PYTHON_ENV_INTERPRETER=bin/python3

if test -f "$PYTHON_ENV_INTERPRETER"; then
	echo "Python local environment with dependencies installed"
else
	echo "Setting up local environment and dependencies"
	python3 -m venv .
	pip install -r requirements.txt
fi

bin/python3 sysrdl2jinja/convert.py $1 templates/sysrdl_adoc_table.template $2

cd -
