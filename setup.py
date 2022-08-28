
"""
Yatse
---------------
Yet another tiny search engine (Yatse) is a easy to use search engine
created purely for fun and learning purposes. Index raw texts or files
and search using simple APIs.
"""

from setuptools import find_packages, setup

requirements = []
with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name="Yatse",
    url="https://github.com/djmgit/yatse",
    license="",
    author="Deepjyoti Mondal",
    description="Yer another tiny search engine",
    download_url="",
    long_description=__doc__,
    zip_safe=False,
    keywords = ['text-processing', 'search-engine', 'search', 'ranking'],
    platforms="any",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Search :: Search-Engine :: text-processing :: ranking',
    ],
    version='0.0.1'
)