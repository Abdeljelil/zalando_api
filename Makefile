populate:
	/bin/bash scripts/init_db.sh
	python3.6 scripts/data_population.py

install:
	make clean
	pip3 install -r requirements.txt
	python3.6 setup.py install
	
test:
	/bin/bash scripts/init_db.sh
	python3.6 scripts/load_dummy_db.py
	nosetests -vv \
	--with-coverage \
	--cover-package=zalando_api \
	--cover-erase \
	--cover-html \
	--cover-branches \
	--cover-min-percentage=100 \
	--cover-xml

clean:
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	rm -rf .coverage build cover compliance/reports dist docs/_build htmlcov MANIFEST nosetests.xml zalando_api.egg-info .tox coverage.xml