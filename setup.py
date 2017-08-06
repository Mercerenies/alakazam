
from setuptools import setup
import os

# https://pythonhosted.org/an_example_pypi_project/setuptools.html
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'alakazam',
    packages = ['alakazam'],
    version = '0.2.0',
    description = 'Functional programming sugar for Python',
    long_description = read("README.rst"),
    author = 'Silvio Mayolo',
    author_email = 'mercerenies@comcast.net',
    license = 'BSD3',
    url = 'https://github.com/Mercerenies/alakazam',
    download_url = 'https://github.com/Mercerenies/alakazam/archive/0.2.0.tar.gz',
    keywords = ['functional', 'sugar', 'syntax', 'lambda', 'stream', 'alakazam'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
