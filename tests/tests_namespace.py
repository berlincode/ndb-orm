# -*- coding: utf-8 -*-
# vim: sts=2:ts=2:sw=2

# simple test to work with multiple namespaces / multi tenancy

from unittest import TestCase, main

import os
import ndb_orm as ndb
from google.cloud.datastore_v1.proto import entity_pb2

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

ndb.enable_use_with_gcd(project=PROJECT, namespace="namespace3")

class Department(ndb.Model):
  name = ndb.StringProperty()

class Namespace(TestCase):

  def test_explicit_namespace(self):

    # create two departments with the same id which will be stored in different namespaces
    department1 = Department(
      id="dept_id",
      namespace="namespace1",
      name="department in 'namespace1'",
    )

    department2 = Department(
      id="dept_id",
      namespace="namespace2",
      name="department in 'namespace2'",
    )

    department3 = Department(
      # no namespace here, so the default should be taken (supplied with ndb.enable_use_with_gcd())
      id="dept_id",
      name="department in 'namespace3'",
    )

    if USE_DATASTORE:
      from google.cloud import datastore
      from .gcloud_credentials import EmulatorCredentials

      client = datastore.Client(project=PROJECT, credentials=EmulatorCredentials(), namespace='namespace_xxx') # set default namespace

      client.put(department1)
      client.put(department2)
      client.put(department3)

      key1=ndb.Key(Department, "dept_id", project=PROJECT, namespace="namespace1")
      key2=ndb.Key(Department, "dept_id", project=PROJECT, namespace="namespace2")
      key3=ndb.Key(Department, "dept_id", project=PROJECT, namespace="namespace3")

      department1_from_db = client.get(key1)
      department2_from_db = client.get(key2)
      department3_from_db = client.get(key3)

      self.assertEqual(department1_from_db.name, "department in 'namespace1'")
      self.assertEqual(department2_from_db.name, "department in 'namespace2'")
      self.assertEqual(department3_from_db.name, "department in 'namespace3'")

    else:
      print("skipping test without datastore")

if __name__ == '__main__':
  main()
