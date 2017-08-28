Python-NDB-ORM
==============

NDB-ORM is a python3 compatible orm for google cloud datastore based on ndb.model (create by Guido van Rossum) and
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


Quick Start
-----------

$ pip install --upgrade ndb-orm


Simple example with 
-------------------

```python
    #!/usr/bin/env python

    import ndb_orm as ndb

    class Greeting(ndb.Model):
        """Models an individual Guestbook entry with content and date."""
        content = ndb.StringProperty()
        date = ndb.DateTimeProperty(auto_now_add=True)

```

Most propety types should work just fine. Even the StructuedProperty class, and the 'indexed', 'repeated', 'compression' and 'required' keywords
should be ok.

Enjoy this beautil ORM !

Public repository
-----------------

https://github.com/berlincode/ndb-orm


License
-------

Copyright "the ndb authors" and Ulf Bartel. Code is licensed under the
[Apache 2.0](./LICENSE.txt).
