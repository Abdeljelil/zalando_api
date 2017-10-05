# export PYTHONASYNCIODEBUG=1
# export PYTHONWARNINGS=default
#--cover-min-percentage=85 \

test:
	nosetests -vv \
	--with-coverage \
	--cover-package=zalando_api \
	--cover-erase \
	--cover-html \
	--cover-branches \
	--cover-xml
	
isort:
	isort --check-only --recursive zalando_api

flake8:
	flake8 zalando_api/ --max-complexity=10  --count --max-line-length=80 --import-order-style=google

install:
	make clean
	pip3 install -r requirements.txt
	python3.6 setup.py install
	
clean:
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	rm -rf .coverage build cover compliance/reports dist docs/_build htmlcov MANIFEST nosetests.xml zalando_api.egg-info .tox coverage.xml