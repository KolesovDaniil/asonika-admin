compile_requirements:
	pip-compile requirements.in -o requirements.txt --quiet --no-header --no-emit-index-url

upgrade_requirements:
	pip-compile requirements.in -o requirements.txt --upgrade --quiet --no-header --no-emit-index-url

install_requirements:
	pip install -r requirements.dev.txt --upgrade --use-deprecated=legacy-resolver
