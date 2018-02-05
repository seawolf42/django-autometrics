# -------------------------------------
# MAKEFILE
# -------------------------------------


#
# environment
#

ifndef VIRTUAL_ENV
$(error VIRTUAL_ENV is not set)
endif

ifeq (test,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "test"
  TEST_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(TEST_ARGS):;@:)
endif


#
# commands for testing
#

PHONY: test.flake8
test.flake8:
	flake8 setup.py autometrics_nonrel

PHONY: test.unittests
test.unittests:
	python setup.py test

PHONY: test
test: test.flake8 test.unittests


#
# commands for virtualenv maintenance
#

PHONY: sitepackages.clean
sitepackages.clean:
	pip freeze | xargs pip uninstall -y

PHONY: sitepackages.install
sitepackages.install:
	pip install .


#
# commands for packaging and deploying to pypi
#

PHONY: readme
readme:
	pandoc -o README.rst README.md

PHONY: package
package: readme
	python setup.py sdist

PHONY: submit
submit: readme
	python setup.py sdist upload -r pypi
