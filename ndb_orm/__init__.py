# -*- encoding: utf-8 -*-
# vim: sts=2:ts=2:sw=2

#
# Copyright 2008 The ndb Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""NDB -- A new datastore API for the Google App Engine Python runtime.

This is a special patched version of ndb named ndb-orm.

Public repository:
https://github.com/berlincode/ndb-orm
"""

__version__ = '0.9.0' # originally based on ndb '1.0.10', but partly sync'ed to newer versions

# errors (originally from google.appengine.api.datastore_errors)
from . import datastore_errors

from .model import (
  Index, ModelAdapter, ModelAttribute,
  ModelKey, MetaModel, Model, Expando,

  # errors (originally errors derived from errors from google.appengine.api.datastore_errors)
  KindError, InvalidPropertyError, UnprojectedPropertyError,
  ReadonlyPropertyError, ComputedPropertyError,

  # properties
  IndexProperty, Property, BooleanProperty,
  IntegerProperty, FloatProperty, BlobProperty,
  TextProperty, StringProperty, PickleProperty,
  JsonProperty, UserProperty,
  KeyProperty, DateTimeProperty,
  DateProperty, TimeProperty,
  StructuredProperty, LocalStructuredProperty,
  GenericProperty, ComputedProperty,
  GeoPtProperty, BlobKeyProperty,

  # classes
  GeoPt
  )

from . import msgprop
from .key import Key, set_default_project_name #, get_default_project_name

from . import key as key_module
from . import entity as entity_module
from . import helpers

DEFAULT_MODEL = None

# for monkey patching
real_entity_from_protobuf = None
real_entity_to_protobuf = None

def enable_use_with_gcd(project=None, namespace=None):
  from google.cloud import datastore
  from google.cloud.datastore.key import Key as DatastoreKey
  from google.cloud.datastore_v1.proto import entity_pb2
  from google.cloud._helpers import _datetime_to_pb_timestamp
  from google.cloud._helpers import _pb_timestamp_to_datetime

  global real_entity_from_protobuf
  global real_entity_to_protobuf

  # for monkey patching
  if not real_entity_from_protobuf:
    real_entity_from_protobuf = datastore.helpers.entity_from_protobuf
  if not real_entity_to_protobuf:
    real_entity_to_protobuf = datastore.helpers.entity_to_protobuf

  def model_from_protobuf_datastore(pb):
    if not pb.HasField('key'):  # Message field (Key)
      return None

    key = datastore.helpers.key_from_protobuf(pb.key)
    try:
      modelclass = Model._lookup_model(key.kind, DEFAULT_MODEL)
    except KindError:
      return None
    entity = modelclass._from_pb(pb, key=key, set_key=False)
    #entity = modelclass._from_pb(pb, key=key, set_key=True)
    entity.key = key
    return entity

  def model_to_protobuf_datastore(entity_of_ndb_model, project, namespace=None):
    if namespace and entity_of_ndb_model._key and (entity_of_ndb_model._key.namespace == None):
        # add namespace
        entity_of_ndb_model._key._namespace = namespace
    entity_of_ndb_model._prepare_for_put()
    entity_of_ndb_model._pre_put_hook()
    pb = entity_of_ndb_model._to_pb()

  #   if entity_of_ndb_model._key is None:
  #     entity_of_ndb_model._key = DatastoreKey(
  #       entity_of_ndb_model._get_kind(),
  #       project=project,
  #       namespace=namespace
  #     )

    key_pb = entity_of_ndb_model._key.to_protobuf()
    pb.key.CopyFrom(key_pb)
    return pb

  def new_entity_from_protobuf(entity_protobuf):
    model = helpers.model_from_protobuf(entity_protobuf)
    if model:
      return model

    return real_entity_from_protobuf(entity_protobuf)

  def new_entity_to_protobuf(entity):
    if isinstance(entity, Model):
      if entity._key and entity._key.namespace:
        ns = entity._key.namespace
      else:
        ns = namespace # default namespace
      return helpers.model_to_protobuf(entity, project, ns)

    return real_entity_to_protobuf(entity)

  if project:
    set_default_project_name(project)

    # enable via monkey patching
    datastore.helpers.entity_from_protobuf = new_entity_from_protobuf
    datastore.helpers.entity_to_protobuf = new_entity_to_protobuf
  else:
    # disable: revert to orginal functions
    datastore.helpers.entity_from_protobuf = real_entity_from_protobuf
    datastore.helpers.entity_to_protobuf = real_entity_to_protobuf

  key_module.KeyBase = DatastoreKey
  entity_module.Entity = entity_pb2.Entity
  entity_module.Property = entity_module.Property
  entity_module.Reference = entity_module.Reference
  helpers.datetime_to_pb_timestamp = _datetime_to_pb_timestamp
  helpers.pb_timestamp_to_datetime = _pb_timestamp_to_datetime
  helpers.model_from_protobuf = model_from_protobuf_datastore
  helpers.model_to_protobuf = model_to_protobuf_datastore
