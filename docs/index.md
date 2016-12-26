# Welcome to feet
**Fast Entitiy Extraction Tool**

[![Build Status][travis_img]][travis_href]
[![Coverage Status][coveralls_img]][coverals_href]
[![Code Health][health_img]][health_href]

---

**Complete documentation coming soon!**

## Overview

Feet is a tool for extracting entities from a text according to dictionaries.
A dictionary gathers terms that are representative of an entity type, e.b. city, country, people or company.

Feet takes benefits of the distributed in-memory database system [Redis](https://www.redis.io).
So It's fast and scalable.

The underlying natural language processing is provided by Python NLTK package.
Japanese has been implemented thanks to the Mecab POS tagger.

On-going work for next version:

* better project packaging and documentation
* more testing
* implement various technics for disambiguition of entities by semantics
analysis including the use of thesauri and machine learning.
* compliant to JSON API interface
* definition of relationships between entities according to grammatical patterns including but not only the definition of intents, facts etc.
* additional languages support: Chinese and Korean

As a bonus, there is a function to extract dates from text in Japanese. Next
version may feature a multi-lingual dates extraction function.

Last but not the least this is WIP so rely on it at your own risk. We should
get a reliable version within a few weeks, along with new exciting features.

## Quick Start

feet supports Python versions 2.7+ and pypy.

### Installing Python

Install [Python](http://www.python.org) by downloading an installer appropriate for your system from
<https://www.python.org/downloads/> and running it.

### Installing pip

If you're using a recent version of Python, pip is most likely installed
by default. However, you may need to upgrade pip to the lasted version:

```bash
$ pip install --upgrade pip
```

If you need to install [pip] for the first time, download [get-pip.py].
Then run the following command to install it:

```bash
$ python get-pip.py
```

### Quick start

**Check your locals**

```bash
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

**Setup Redis**

Use of [Redis](https://www.redis.io) is mandatory and v3+ is recommended. 

**Setup Mecab for Japanese**

Setup [MeCaB](http://mecab.googlecode.com/svn/trunk/mecab/doc/index.html)

You can either use ipadic-utf8 dictionary or neologd dictionary:

* ``apt-get install mecab-ipadic-utf8``
* Setup [neologd dictionary](https://github.com/neologd/mecab-ipadic-neologd)

**Setup Feet**

Download latest version of Feet repository.

```bash
$ git clone https://github.com/Altarika/feet.git
$ cd feet
$ python setup.py install
```

or from pip (TODO):
```bash
$ pip install feet
```

**For development**

Create a virtualenv and install dependencies

```bash
$ virtualenv venv
$ source venv/bin/activate
```

```bash
$ echo $(pwd) > project_venv/lib/python2.7/site-packages/feet.pth
```

Install Python dependencies
```bash
$ pip install -r requirements.txt
```

Check the changelog:
```bash
$ git log --oneline --decorate --color
```

**Setup NLTK**

Depending on the languages you want to use you have to download the necessary
data for NLTK to support them. Please see the documentation of [NLTK](http://www.nltk.org/).
We are using NLTK version 3.0.

```bash
$ python -m nltk.downloader averaged_perceptron_tagger maxent_ne_chunker maxent_treebank_pos_tagger punkt words
 
```

**Configuration**

Setup your environment parameters in feet.yaml after copying config/feet_example.yaml

You can locate the configuration file at: 
/etc/feet.yml
~/.feet.yaml
conf/feet.yaml

Content of configuration file:
```yaml
# Basic Flags
debug: true

# Logging Information
logfile: 'feet.log'
loglevel: 'DEBUG'

# Timeout processing
timeout: 180

# Redis database Information
database:
    host: localhost
    port: 6379
    prefix: feet

# API Server
server:
    host: 127.0.0.1
    port: 8000

# Japanese POS Tagger MeCab
mecab:
    mecabdict= 'usr/local/lib/mecab/dic/mecab-ipadic-neologd'
```

You can also use a .env file:

```
MECAB_DICT=/usr/local/lib/mecab/dic/mecab-ipadic-neologd
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DICT_DB=0
REDIS_PREFIX=feet
DEBUG=True
SERVER_HOST=localhost
SERVER_PORT=8888
LOG_FILE=feet.log
LOG_LEVEL=INFO
TIMEOUT=180
```

If both a YAML and a .env file are available, YAML file will override common
environment variables.

**Testing**

Run the tests to make sure everything is OK.

```bash
$ pip install ./requirements/test.txt
$ nosetests -v --with-coverage --cover-package=feet --cover-inclusive --cover-erase tests ./feet/www/tests/
```

or with Tornado testing tools:

```bash
$ python -m tornado.testing  discover
```
 
or with setuptools
```bash
$ python setup.py test
```

## Read the doc

You can generate a documentation with mkdocs tool.

Install the mkdocs package using pip:

```bash
$ pip install mkdocs
```

Install Yeti theme from mkdocs-bootswatch: 

```bash
$ pip install mkdocs-bootswatch
```

You should now have the mkdocs command installed on your system. 
Run mkdocs --version to check that everything worked okay.

```bash
$ mkdocs --version
mkdocs, version 0.15.2
```

Launch the documentation server:

```bash
$ mkdocs serve
```

Then open your browser on http://127.0.0.1:8000/

## CLI

Follow the Quick Start instructions. Make sure a redis-server is running.
Make and update your favorite configuration file (.env or yml).

From feet directory you can use ``$ ./bin/feet`` command or you can directly
call ``$ feet`` if you have been through complete installation via setuptools.

**Load** entity file with CLI:
```bash
$ feet load --registry=my_registry --entity=country --csv=./tests/test_data/countries_en.csv
```

**Drop** list of terms for company with CLI:
```bash
$ feet drop --registry=my_registry --entity=country
```

**Extract** entities from a text:
```bash
$ feet extract --registry=my_registry --entity=country --grammar="NE : {<NNP|NNPS|NN>*<DT>?<NNP|NNPS|JJ|NNS|NN>+}" --path=./tests/test_data/english_text_long.txt 
```

or

```bash
$ feet extract --registry=my_registry --entity=country --grammar="NE : {<NNP|NNPS|NN>*<DT>?<NNP|NNPS|JJ|NNS|NN>+}" --text="I want to buy flight tickets for Japan" 
```

## HTTP API server tools

Follow the Quick Start instructions. Make sure a redis-server is running.
Make and update your favorite configuration file (.env or yml).

From feet directory you can use ``$ ./bin/feet`` command or you can directly
call ``$ feet`` if you have been through complete installation via setuptools.

**Feet run !**

Launch the server:
```bash
$ feet run --host=127.0.0.1 --port=8888 
```

Feet proposes a Restful API. It's easy to guess where you are from the url. In order
to manage your entities you can group them into different databases,
prefixes and registries. The database identifier follows Redis rule. A prefix and a registry can be any
alphanumeric urlencoded characters strings.

**Get list of registries**
```bash
curl -H "Accept: application/json" -X GET http://localhost:8888/database/<database>/prefix/<prefix_name>/registries/
--> 200 {"registries":["registry1","registry2"]}
```

**Add a registry**
```bash
curl -H "Content-Type: application/json" -X POST http://localhost:8888/database/<database>/prefix/<prefix_name>/registries/<registry>/
--> 200 OK
```

**Delete a registry**
```bash
curl -H "Content-Type: application/json" -X DELETE http://localhost:8888/database/<database>/prefix/<prefix_name>/registries/<registry>/
--> 200 OK
```

**Get list of registered entities**
```bash
curl -H "Accept: application/json" -X GET http://localhost:8888/database/<database>/prefix/<prefix_name>/registries/<registry>/entities/
```
Example:
```bash
http://localhost:8888/database/0/prefix/geographic/registry/my_registry/entities/
--> 200 {"entities":["city","country"]}
```

**Add an entity**
```bash
curl -H "Content-Type: application/json" -X POST http://localhost:8888/database/<database>/prefix/<prefix_name>/registries/<registry>/entities/<entity_name>/
--> 200 OK
```

**Delete an entity**
```bash
curl -H "Content-Type: application/json" -X DELETE http://localhost:8888/database/<database>/prefix/<prefix_name>/registries/<registry>/entities/<entity_name>/
--> 200 OK
```

**Getting an entity provides the list of languages supported by the entity**
```bash
curl -H "Accept: application/json" -X GET http://localhost:8888/database/<database>/prefix/<prefix_name>/registries/<registry>/entities/<entity_name>/
--> 200 {"languages":["english"]}
```

**Add a language for an entity**
```bash
curl -H "Content-Type: application/json" -X POST http://localhost:8888/database/<database>/prefix/<prefix_name>/registries/<registry>/entities/<entity_name>/lang/<lang_id>/
--> 200 OK
```

The list of language identifiers that we use comes from NLTK. You must follow
this list if you want feet to branch correctly into NLTK. 

**Delete a language for an entity**
```bash
curl -H "Content-Type: application/json" -X DELETE http://localhost:8888/database/<database>/prefix/<prefix_name>/registries/<registry>/entities/<entity_name>/lang/<lang_id>/
--> 200 OK
```

**Geting a language provides the number of terms for this language**
```bash
curl -H "Accept: application/json" -X GET http://localhost:8888/database/<database>/prefix/<prefix_name>/registries/<registry>/entities/<entity_name>/lang/<lang_id>/
--> 200 {"count":249}
```

This allows to get the total number of terms for a language.

**Change the name of language**
```bash
curl -H "Content-Type: application/json" -X PUT -d '{"new_name": "english"}'
http://localhost:8888/database/<database>/prefix/<prefix_name>/registries/<registry>/entities/<entity_name>/lang/<lang_id>/
--> 200 OK 
```

**Create/add list of terms**
```bash
curl -H "Content-Type: application/json" -X POST/PUT -d '{"entities": ["Paris","Tokyo"]}' http://localhost:8888/database/<database>/prefix/<prefix_name>/registries/<registry>/entities/<entity_name>/lang/<lang_id>/terms/
--> 200 OK
```

**Get list of terms for an entity and a language**
```bash
curl -H "Accept: application/json" -X GET -d '{"page":0,"count":10}' http://localhost:8888/database/<database>/prefix/<prefix_name>/registries/<registry>/entities/<entity_name>/lang/<lang_id>/terms/?page=0&count=10
--> 200 {"terms":["Paris","Tokyo"]}
```

**Delete all terms for an entity and a language**
```bash
curl -H "Content-Type: application/json" -X DELETE -d '{"entities": ["Paris"]}' http://localhost:8888/database/<database>/prefix/<prefix_name>/entities/<entity_name>/languages/<lang_id>/terms/
--> 200 OK
```

**Get a term**
```bash
curl -H "Accept: application/json" -X GET http://localhost:8888/database/<database>/prefix/<prefix_name>/registries/<registry>/entities/<entity_name>/lang/<lang_id>/terms/Tokyo/
--> 200 Tokyo
```

**Add a term**
```bash
curl "Content-Type: application/json" -X POST  http://localhost:8888/database/<database>/prefix/<prefix_name>/registries/<registry>/entities/<entity_name>/lang/<lang_id>/terms/Tokyo/
--> 200 OK
```

**Delete a term**
```bash
curl "Content-Type: application/json" -X DELETE 
http://localhost:8888/database/<database>/prefix/<prefix_name>/registries/<registry>/entities/<entity_name>/lang/<lang_id>/terms/Tokyo/
--> 200 OK
```

**Extract entities from a text**
```bash
curl -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"test":"I am looking for tickets for Tokyo in Japan", "grammar":"NE : {<NNP|NNPS|NN>*<DT>?<NNP|NNPS|JJ|NNS|NN>+}"}'
http://localhost:8888/database/0/prefix/geographic/entities/city/languages/english/extract/
--> 200 {"result":["Tokyo"]}
```

**TODO: Search for entities**
```bash
curl -H "Accept: application/json" -H "Content-Type: application/json" -X GET
http://localhost:8888/database/0/prefix/geographic/entities/city/languages/english/search?q=Tok&page=0&count=10
--> 200 {"result":["Tokyo"]}
```

## How to use

Follow the quick start installation.

Using Feet relies on three classes:

* Registry
* Dictionary
* Extractor

(Don't forget to run a Redis server)

### Key prefix

Before talking about the classes it's important to explain the concept of key
prefix. As we are using a Redis database to store all data they can be organized
by a key prefix. It means that all keys used to store information about
registries, dictionaries etc. will be prefixed. It provides you with a first
level of organisation for your data.

```
+------------------------------------+
|  +-------------------------------+ |
|  |  +--------------------------+ | |
|  |  |                          | | |
|  |  |     Term                 | | |
|  |  |                          | | |
|  |  | Entity/Dictionary        | | |
|  |  +--------------------------+ | |
|  |Registry                       | |
|  +-------------------------------+ |
|Key prefix                          |
+------------------------------------+
```

### Registries

Each registry manages a list of dictionaries. It's a second level of
organisation after key prefixes.

Get the list of registries for a specific key prefix:

```python
from feet.entities.registry import Registry

registries = Registry.list(key_prefix='my_prefix')
```

Add a registry:

```python
from feet.entities.registry import Registry

registry = Registry.find_or_create('my_registry',
    key_prefix='my_prefix',
    redis_host='127.0.0.1',
    redis_port=6379,
    redis_db=0)
```

Get the list of dictionaries in a registry:

```python
registry.dictionaries()
```

Add/get a dictionary in a registry:

```python
# dictionary is ot type Dictionary by default
dictionary = registry.get_dict('entity_name')
```

Delete a dictionary:

```python
registry.del_dict('entity_name')
```

Delete a registry:

```python
# This will automatically delete all related dictionaries
registry.delete()
```

### Make a dictionary for an entity

```python
from __future__ import print_function
from feet.entities.registry import Registry

# Get an entity dictionary
registry = Registry.find_or_create('my_registry',
    key_prefix='test_feet',
    redis_host='127.0.0.1',
    redis_port=6379,
    redis_db=0)
entity = registry.get_dict('events')

# Load a file that contains a list of entities
count = entity.load_file('./test_data/events_ja.txt')
print('%d entities imported' % count)
```

where 'events_ja.txt' file contains a list of marketing events with each event
name on a different line.

load_file method returns the number of terms that have been succesfully
imported.

If you want to deal with different file formats you can inherit from Dictionary
and override get_entities method. It could be as simple as:

```python
from __future__ import print_function
from feet.entities.registry import Registry
from feet.entities.dictionary import Dictionary

class MyDictionary(Dictionary):
    def get_entities(self, entities_file):
        handle = open(entities_file, "r")
        for entity in handle.readlines():
          yield entity

# Get an entity dictionary
registry = Registry.find_or_create('my_registry',
    dict_class=MyDictionary,
    key_prefix='test_feet',
    redis_host='127.0.0.1',
    redis_port=6379,
    redis_db=0)
entity = registry.get_dict('my_entity')

# Load a file that contains a list of entities
count = entity.load_file('my_formatted_file.my')
print('%d entities imported' % count)
``` 

This will allow you to build your own importers for different formats e.g. 
JSON, CSV, XML, RDF etc.

A CSV import tool is available as CSVDictionary in feet.entities.dictionary:

```python
from __future__ import print_function
from feet.entities.dictionary import CSVDictionary

registry = Registry.find_or_create('my_registry',
  dict_class=CSVDictionary)
cities = registry.get_dict('cities')
count = cities.load_file('./test_data/world-cities.csv') 
```

### Extract entities from a text with a dictionary

```python
from __future__ import print_function
from feet.entities.extractor import Extractor
from feet.entities.dictionary import CSVDictionary

registry = Registry.find_or_create('my_registry',
  dict_class=CSVDictionary)
cities = registry.get_dict('cities')
count = cities.load_file('./test_data/world-cities.csv') 

# Get an entity extractor engine
# Specify a grammar to extract chunks of candidates for 'NE' Named Entities
extractor = Extractor(
    ref_dictionary=cities,
    grammar='NE : {<NNP|NNPS|NN>*<DT>?<NNP|NNPS|JJ|NNS|NN>+}')
# Ask for entities from a text (it must be UTF8 encoded)
result = extractor.extract(utf8_encoded_text)

# Display results
entities = []
for element in results[0]:
    if element['entity_found'] == 1:
      entities = list(set(entities).union(element['entity_candidates']))
print(entities)
```

### Bonus: Extracting dates in Japanese

```python
from feet.entities.jptools import JAParser

dates = JAParser().extract_dates(utf8_encoded_text)
```

## Deploy with Docker

Make sure the REDIS_HOST in your configuration file (see Quick start
configuration section) is set to the name of redis service defined in the
docker_compose.yml file. For example:

```
REDIS_HOST=redis
```

Double check that SERVER_PORT matches the open port of your container as
defined in docker-compose.yml file. For example:

```
SERVER_PORT=5000
```

Start a container for development (version of docker-compose > v1.9.0):

```bash
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

The Dockerfile describes an image that includes Neologd dictionary. Installation
of Neologd takes time and space, however it will provide the best quality in
terms of entity extraction. You can also rely only on macacb-ipadic-utf8 by
commenting this line in Dockerfile:

```
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git && cd mecab-ipadic-neologd && ./bin/install-mecab-ipadic-neologd -y 
```

Make sure that either .env and/or feet.yaml configuration files specify the
right path to access the dictionary:

In feet.yaml:
```yaml
# Japanese POS Tagger MeCab
mecab:
    mecabdict= '/usr/lib/mecab/dic/mecab-ipadic-neologd'
```

In .env:
```
MECAB_DICT=/usr/local/lib/mecab/dic/mecab-ipadic-neologd
``` 

## Getting help

To get help with feet, please contact Romary on romary.dupuis@altarika.com


<!-- References -->
[travis_img]: https://travis-ci.org/Altarika/feet.svg?branch=develop
[travis_href]: https://travis-ci.org/Altarika/feet/
[coveralls_img]: https://coveralls.io/repos/github/Altarika/feet/badge.svg?branch=develop
[coverals_href]: https://coveralls.io/github/Altarika/feet?branch=develop
[health_img]: https://landscape.io/github/Altarika/feet/develop/landscape.svg?style=flat
[health_href]: https://landscape.io
