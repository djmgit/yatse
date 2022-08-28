# Yatse

Yatse stands for Yet another tiny search engine. As the name suggests Yatse is a tiny, minimalistic seatch engine created from scratch in python.
It uses Redis (cluster mode supported) for storing the indexes. Yatse is build purely for fun and learning purposes.

## Getting started

Yatse is not available on pip. I might release it someday after playing around a bit more and adding some more stuff. Till then it can be installed
from source.

- Launch your terminal
- git clone this repository and navigate to project root.
- Run ```python3 setup.py install```
- Conversely you can also ```pip3 install -e .```. This will symlink to your source directory, pretty usefull when developing.

Yatse should be installed in your system now. Next you will have to start Redis. You can do it in a number of ways like docker, build from source
or simply use your package manager to install it. I use ```apt install redis-server``` to install it since I use ubuntu and use systemd to mange'
the Redis process. Anyways, once redis is up and running make sure you are able to connect to the server using redis-cli.

Now we are all set to try out Yatse.

## Indexing some documents

Lets start by indexing some raw texts.

Launch your terminal. Create a directory, something like data or yatse_data using ```mkdir yatse_data```. Yatse will use this directory to store all
the raw texts we will be indexing. If we want to directly index some files then the files need to be present inside this directory. Yatse does not
support hirarchy, it assumes all files are present flat in the data directory. I wanted to keep it as simple as possible.
Next, lauch python in REPL mode and punch in the following.

```
from yatse import Yatse
import logging

yatse = Yatse(data_path="yatse_data", log_level=logging.INFO)
yatse.index("test-1", "Yatse is a tiny search engine. It has been created for fun and learning")
yatse.index("test-2", "Yatse is extremely minimal. It can be used as a lib")
yatse.index("test-3", "Yatse uses redis to store its indexes better known as inverted inverted index")
yatse.index("test-4", "Yatse will store all these texts as flat files under data_path")

```
In the above snippet we indexed 4 documents


