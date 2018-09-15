# -*- coding: utf-8 -*-
# vim: sts=2:ts=2:sw=2

from unittest import TestCase, main

import os
import ndb_orm as ndb

USE_DATASTORE = False # default

if 'DATASTORE_ENV_YAML' in os.environ:
  print("\n!!! using datastore emulator !!!")
  import yaml

  with open(os.environ['DATASTORE_ENV_YAML']) as fhandle:
    datastore_emulator_env_vars = yaml.load(fhandle.read())
  datastore_emulator_env_vars = {key: value.replace('::1', 'localhost') for key, value in datastore_emulator_env_vars.items()}
  os.environ.update(datastore_emulator_env_vars)
  USE_DATASTORE = True
  PROJECT = datastore_emulator_env_vars['DATASTORE_PROJECT_ID']
else:
  PROJECT = "your-project"

ndb.enable_use_with_gcd(project=PROJECT)

class Person2(ndb.Model):
  name = ndb.TextProperty(indexed=True)
  age = ndb.IntegerProperty(indexed=True)

class SimpleQuery(TestCase):

  def test_simple_query(self):
    if not USE_DATASTORE:
      print('skipping test')
      return 

    from google.cloud import datastore
    from .gcloud_credentials import EmulatorCredentials
    client = datastore.Client(project=PROJECT, credentials=EmulatorCredentials())

    person = Person2(
      id="guido_12",
      name="Guido",
      age=12,
    )
    client.put(person)

    # use google datastore for creating queries
    qry = client.query(
      kind=Person2._get_kind() # pylint:disable=protected-access
    )
    self.assertEqual(len(list(qry.fetch())), 1)

    # now add a filter
    qry2 = client.query(
      kind=Person2._get_kind(), # pylint:disable=protected-access
      filters=[
          (Person2.age._name, "<=", 100), # pylint:disable=protected-access
      ],
    )
    self.assertEqual(len(list(qry2.fetch())), 1)

    # now add a filter
    qry2 = client.query(
      kind=Person2._get_kind(), # pylint:disable=protected-access
      filters=[
          (Person2.age._name, ">", 100), # pylint:disable=protected-access
      ],
    )
    self.assertEqual(len(list(qry2.fetch())), 0)

if __name__ == '__main__':
  main()
