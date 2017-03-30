import os

from setuptools import find_packages, setup


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='djangae-rest-autometrics',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A Django+Djangae app to collect session and access metrics.',
    long_description=README,
    url='https://google.com/',
    author='jeffrey k eliasen',
    author_email='jeff@jke.net',
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
    install_requires=[
        'Django>=1.8,<1.9',
        'djangae>=0.9.8',
        # 'djangorestframework',
    ],
)
