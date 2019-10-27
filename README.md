# Planyo

*Python client for Planyo API*

### Description

Planyo API low level client. Provides a straightforward mapping from Python to Planyo REST endpoint.


### Requisites

Python 2.7+ or 3


### Install

```bash
pip install -e git+https://github.com/chesstrian/planyo-py.git#egg=planyo
# or, for private repos:
pip install -e git+git@github.com:chesstrian/planyo-py.git#egg=planyo
```


### Usage

```python
from planyo import Planyo

client = Planyo(api_key='ABC')
client.api_test()
```

The instance has all methods present in Planyo API Docs: https://api.planyo.com/api.php

It is highly recommended to checks docs for params received by any method. Just pass a dictionary in `params` with
all desired arguments.

```python
from planyo import Planyo

client = Planyo(api_key='ABC')
client.api_test(params=dict(language='IT'))
```

Hash key is also supported, in this case the instance needs to be initialized with the secret hash key from Planyo

```python
from planyo import Planyo

client = Planyo(api_key='ABC', hash_key='DEF')
client.api_test()
```


### Tests

```bash
python tests.py
```
