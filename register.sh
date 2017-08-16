pip install pandoc || exit
pandoc -o README.rst README.md || exit
python setup.py sdist upload -r pypi
