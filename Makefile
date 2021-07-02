compile_requirements:
	pip-compile requirements.in -o requirements.txt --quiet --no-header --no-emit-index-url

upgrade_requirements:
	pip-compile requirements.in -o requirements.txt --upgrade --quiet --no-header --no-emit-index-url

install_requirements:
	pip install -r requirements.dev.txt --upgrade

format:
	isort .
	black .

check:
	isort --check-only --diff .
	black --check .
	flake8 --config=flake8.ini
	bandit . --recursive --quiet --exclude **/tests*,./.venv,./venv
	mypy .
