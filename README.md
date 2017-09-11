Python-NDB-ORM
==============

[![Travis CI](https://travis-ci.org/berlincode/ndb-orm.svg?branch=master&style=flat)](https://travis-ci.org/berlincode/ndb-orm)
[![Python versions](https://img.shields.io/pypi/pyversions/ndb-orm.svg)](https://pypi.python.org/pypi/ndb-orm/)
[![Apache License 2.0](https://img.shields.io/pypi/l/ndb-orm.svg)](https://github.com/berlincode/ndb-orm/blob/master/LICENSE.txt)

NDB-ORM is a python3 compatible orm for google cloud datastore based on ndb.model (created by Guido van Rossum) and
may be used outside of app engine standard environment.

 * Plays nicely with datastore entities generated from app engine standard
 * Python3 compatible
 * Usable from outside of app engine standard
 * Based on the original ndb package
 * Protobuffer implementation was ported to google.cloud.proto.datastore.v1.entity_pb2 (which is also used by gcloud-datastore-python)
 * No dependencies to old appengine libraries
 * Makes porting of app engine standard project easier
 * Works with [google-cloud-datastore](https://pypi.python.org/pypi/google-cloud-datastore)
 * Key handling is used from google.cloud.datastore

This is not a drop-in replacement for the whole ndb package (no ndb.context, ndb.tasklets, ndb.query or ndb.Key), 
but allows you to use ndb.model classes.

For more details of all the possobilities of the ndb.model orm, plead have a look at "[The Python NDB Client Library Overview](https://cloud.google.com/appengine/docs/standard/python/ndb/)".

ATTENTION
-----------

While reading of entities generated with app engine standard should be no problem, threre are limitations reading
entities written with this package (also also with google-cloud-datastore) from app engine standard. The reason is that
some types have changed format (e.g. datetime properties with google-cloud-datastore support timezones).

Additional (as you might have expected) using the PickleProperty between different Python version
is expected to fail and thus pickle.loads is disabled by default. You can enable it by setting
ndb_orm.model.ENABLE_PICKLE_LOADS to True.

Quick Start
-----------

$ pip install --upgrade ndb-orm


Simple example session with google-cloud-datastore 
--------------------------------------------------

```python
>>> #
>>> # creating an entity with google-cloud-datastore
>>> #

>>> from google.cloud import datastore
>>> 
>>> client = datastore.Client()
>>> 
>>> kind = 'Task' # The kind for the new entity
>>> name = 'sampletask' # The name/ID for the new entity
>>> 
>>> key = client.key(kind, name) # The Cloud Datastore key for the new entity
>>> 
>>> entity = datastore.Entity(key=key, exclude_from_indexes=('text',))
>>> entity.update({
...     'text': 'Much to do',
...     'done': False,
... })
>>> 
>>> client.put(entity)

>>> #
>>> # now getting the just saved entity as ndb.Model by defining an entity
>>> # 'Task' and enabling ndb_orm
>>> #

>>> import ndb_orm as ndb
>>> ndb.enable_use_with_gcd(client.project)
>>> 
>>> class Task(ndb.Model):
...     text = ndb.TextProperty(indexed=False)
...     done = ndb.BooleanProperty()
...     update = ndb.DateTimeProperty(auto_now=True)
>>> 
>>> entity = client.get(key) # now get get an ndb model for the same data ! 
>>> print(entity)
Task(key=<Key('Task', 'sampletask')>, done=False, text='Much to do')
>>>
>>> client.put(entity) # save entity ('update' property gets set automatically)
>>>
>>> print(client.get(key)) # get entity with 'update' property set
Task(key=<Key('Task', 'sampletask')>, done=False, text='Much to do', update=datetime.datetime(2017, 8, 28, 22, 16, 15, 652839, tzinfo=<UTC>))
 
>>> #
>>> # access to this entity without ndb-orm still possible
>>> #

>>> ndb.enable_use_with_gcd() # disable ndb-orm - now we wont receive a ndb.Model anymore
 
>>> print(client.get(key)) # a normale get still works without ndb-orm
<Entity('Task', 'sampletask') {'done': False, 'update': datetime.datetime(2017, 8, 28, 22, 16, 15, 652839, tzinfo=<UTC>), 'text': 'Much to do'}>
>>> 
```

Most property types should work just fine. Even the StructuredProperty class, and keywords 'indexed', 'repeated', 'compression', 'name' and 'required'
should work as well.

Enjoy this beautiful ORM !

Public repository
-----------------

[https://github.com/berlincode/ndb-orm](https://github.com/berlincode/ndb-orm)


License
-------

Copyright "the ndb authors" and Ulf Bartel. Code is licensed under the
[Apache 2.0](./LICENSE.txt).
