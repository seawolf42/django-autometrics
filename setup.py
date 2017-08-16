import os
import subprocess
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


class DjangoTestAndLint(TestCommand):

    description = 'run linters and tests'
    user_options = []

    def run_tests(self):
        self._run([
            'flake8',
            'autometrics_nonrel',
            'manage.py',
            'settings.py',
            'setup.py',
            'wsgi.py',
            ])
        self._run(['python', 'manage.py', 'test', '-v 2'])

    def _run(self, command):
        try:
            subprocess.check_call(command)
        except subprocess.CalledProcessError as error:
            print('Command failed with exit code', error.returncode)
            sys.exit(error.returncode)


install_dependencies = [
    'Django>=1.8,<1.9',
    'djangae>=0.9.10',
]

setup(
    name='django-autometrics-nonrel',
    version='0.9.3',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A Django+Djangae app to collect session and access metrics.',
    long_description=README,
    url='https://github.com/seawolf42/django-autometrics',
    author='jeffrey k eliasen',
    author_email='jeff+django-autometrics@jke.net',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Logging',
    ],
    keywords='django analytics',
    install_requires=install_dependencies,
    tests_require=install_dependencies + [
        'flake8',
        'mock',
    ],
    cmdclass={
        'test': DjangoTestAndLint,
    },
)
