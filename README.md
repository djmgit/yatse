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
or simply use your package manager to install it. I used ```apt install redis-server``` to install it since I use ubuntu and use systemd to mange'
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

Following parameters are supported by the Yatse class contsructor:

- redis_host: the redis host, defaults to 127.0.0.1
- redis_port: the redis port, defaults to 6379
- cluster_mode: if you are running redis in cluster mode, defaults to False
- data_path: The directory path where Yatse will store all raw texts as documents. If you are indexing files directly, then Yatse will assume they are
             present here.
- log_level: Standard log levels exposed by python logging module. Defaults to logging.INFO.

index function is called with two parameters, the document_id and the document_body. If the document_body is not present then yatse assumes that the
document is present under data_path and tries to read and index it.

Indexing roughly works in the following way:

- First it will save the text with name as the document identifier under data_path.
- Next it will process the text, which includes the usual stuff like removing the punctuations, converting it to lowercase.
- Stemming is a very popular step while dealing with natural language (mostly english) wherein we extract word roots. For example running becomes run, walked becomes walk etc. However for yatse I chose to go with **edge-ngrams**.
- Whats edge-ngram? Lets first understand whats **ngram**. Ngrams are the tokens generated from a word by moving a window of a fixed size over it. For example lets consider the word "python". If our ngram window size is 3 then the generated ngrams would be "pyt", "yth", "tho", "hon"
- Edge-ngram is a modification of ngrams where in instead of moving the window, the left end of the window is kept fixed at the left edge of the world, we start with a fixed size and keep increasing the window size until we reach the end of the word. For example lets once again consider the word "python" and edge-ngram window start size to be 3. Then the edge-ngrams we end up with are "pyt", "pyth", "pytho", "python".
- Stemming is sometimes a tricky process for certain words whereas edgie-ngrams allows us to do fuzzy search as well. A obvious drawback of this process is the number of indexed terms increases.
- Coming back to our indexing process, we create edge-ngrams out of our bag words.
- Next, we find out where all in the processed text the word containing the edge-ngram occurs and we create a list for that. Finally we create the index in redis by storing the term along with the documents where it has occured as well as the positions in each document.

An example term in redis would look something like:
```
"term_xyz": {
  # "documet-id": "[positions]"
  "document-1": "[0, 1, 5, 10],
  "document-4": "[1, 8]"
}

```
Not to mention each term is a hashset in redis. I could have made each term the root key of a global hashset but I chose to keep them individually in the root space so that in case of redis cluster the terms can get automatically sharded without much of an effort.

Now we have our inverted index created, ready to be searched.

## Searching our index

Searching is also pretty straight forward.

```
# you have already created an intance of yatse and indexed some texts or files
# yatse = Yatse(.......)
# yatse.index(.....)
# yatse.index(.....)

print (yatse.search("what is yatse"))

'''
It should give a response of the following format:
{
        "total_matched_docs": 1,
        "time_taken_seconds": <epoch_difference>,
        "time_taken_human_readable": <epoch_diff_in_hh:mm:ss_format>
        "documents": [{
            "relevence_score": 0.005,
            "document_name": doc-1,
            "document_full_path": /tmp/doc-1,
            "occurence_count": 5
        }]
}
'''

```

search function additionally accepts a limit parameter to limit number of results returned.

Search roughly works in the following way:

- Inital steps are pretty much similar to that of indexing.
- We first process the query, that is remove punctuations and created edge-ngrams out of it.
- Next we extract the term data from redis.
- We find out the matched documents and calculate **bm25 relevance** score for each document. Then we sort the documents in descending order with respect to the bm25 relevance score.
- We also calculate the time taken to generate the response.
