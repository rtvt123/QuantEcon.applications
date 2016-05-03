# Make Files for QuantEcon.applications

test-ipynb:
	python ./_scripts_/test-ipynb.py

test-py:
	python ./_scripts_/test-py.py

test:
	make test-ipynb
	make test-py