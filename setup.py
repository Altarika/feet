from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import os
import sys
import re
import codecs

# Basic information
NAME = 'feet'
DESCRIPTION = 'Feet - Fast Entity Extraction Tool'
AUTHOR = 'Romary Dupuis'
EMAIL = 'romary.dupuis@altarika.com'
MAINTAINER = 'www.altarika.com'
MAINTAINER_EMAIL = EMAIL
LICENSE = 'LGPL'
REPOSITORY = 'https://github.com/Altarika/feet/'
PACKAGE = 'feet'

# Define the keywords
KEYWORDS = ('nlp', 'feet', 'entity', 'redis', 'NER')

# Important paths
PROJECT = os.path.abspath(os.path.dirname(__file__))
PKG_DESCRIBE = "DESCRIPTION.txt"

here = os.path.abspath(os.path.dirname(__file__))

src_root = os.curdir

packages = find_packages(src_root, include=['feet', 'feet.*'])


def get_version(package):
    """Return package version as listed in `__version__` in `version.py`."""
    init_py = open(os.path.join(package, 'version.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    """Return root package and all sub-packages."""
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def read(*parts):
    """
    Assume UTF-8 encoding and return the contents of the file located at the
    absolute path from the REPOSITORY joined with *parts.
    """
    with codecs.open(os.path.join(PROJECT, *parts),
                     'rb', 'utf-8') as f:
        return f.read()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


if sys.argv[-1] == 'publish':
    if os.system('pip freeze | grep wheel'):
        print('wheel not installed.\nUse `pip install wheel`.\nExiting.')
        sys.exit()
    if os.system('pip freeze | grep twine'):
        print('twine not installed.\nUse `pip install twine`.\nExiting.')
        sys.exit()
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    print('You probably want to also tag the version now:')
    print("  git tag -a {0} -m 'version {0}'".format(get_version('feet')))
    print('  git push --tags')
    sys.exit()

setup(
    name=NAME,
    version=get_version(PACKAGE),
    url=REPOSITORY,
    license=LICENSE,
    author=AUTHOR,
    author_email=EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    tests_require=['pytest'],
    install_requires=['python-dotenv',
                      'tornado>=4.1',
                      'redis',
                      'nltk>=3',
                      'mecab-python',
                      'langdetect',
                      'dateparser',
                      'numpy',
                      'click',
                      'confire==0.2.0',
                      'PyYAML==3.11',
                      'commis==0.2',
                      'colorama==0.3.6',
                      'mkdocs'
                      ],
    cmdclass={'test': PyTest},
    description=DESCRIPTION,
    long_description=read('DESCRIPTION.txt'),
    packages=packages,
    include_package_data=True,
    src_root=src_root,
    platforms='any',
    entry_points={
        'console_scripts': [
            'feet = feet.__main__:cli',
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 1 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: LGPL',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords=KEYWORDS,
    extras_require={
        'testing': ['pytest'],
    }
)
