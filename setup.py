import os, json, imp
from setuptools import setup, find_packages

PROJ_NAME = 'arduino'
PACKAGE_NAME = 'arduino'
PROJ_METADATA = 'info.json'


here = os.path.abspath(os.path.dirname(__file__))
proj_info = json.loads(open(os.path.join(here, PROJ_METADATA), encoding='utf-8').read())

CHANGELOG = open(os.path.join(here, 'CHANGELOG.rst'), encoding='utf-8').read()

try:
    README = open(os.path.join(here, 'README.rst'), encoding='utf-8').read()
except FileNotFoundError:
    README = ""

setup(
    name=proj_info['name'],
    version=proj_info['VERSION'],
    author=proj_info['author'],
    author_email=proj_info['author_email'],
    url=proj_info['url'],
    license=proj_info['license'],
    
    description=proj_info['description'],
    keywords=proj_info['keywords'],
    
    classifiers=proj_info['classifiers'],
    
    packages=find_packages('src'),
    package_dir={'': 'src'},

    install_requires=[''],
    entry_points={
    }
)
