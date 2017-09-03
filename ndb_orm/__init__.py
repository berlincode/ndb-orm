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

__version__ = '0.5.0' # originally based on ndb '1.0.10', but partly sync'ed to newer versions

from google.cloud import datastore
from google.cloud.datastore.key import Key as DatastoreKey

# errors (originally from google.appengine.api.datastore_errors)
from . import datastore_errors

from .model import (
  DEFAULT_PROJECT_NAME,

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

DEFAULT_MODEL = None

# for monkey patching
real_entity_from_protobuf = datastore.helpers.entity_from_protobuf
real_entity_to_protobuf = datastore.helpers.entity_to_protobuf

def model_from_protobuf(pb):
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

def model_to_protobuf(entity_of_ndb_model, project, namespace=None):
  entity_of_ndb_model._prepare_for_put()
  pb = entity_of_ndb_model._to_pb()

  if entity_of_ndb_model._key is None:
    entity_of_ndb_model._key = DatastoreKey(
      entity_of_ndb_model._get_kind(),
      project=project,
      namespace=namespace
    )

  entity_of_ndb_model._pre_put_hook()
  key_pb = entity_of_ndb_model._key.to_protobuf()
  pb.key.CopyFrom(key_pb)
  return pb

def enable_use_with_gcd(project=None, namespace=None):
  def new_entity_from_protobuf(entity_protobuf):
    model = model_from_protobuf(entity_protobuf)
    if model:
      return model

    return real_entity_from_protobuf(entity_protobuf)

  def new_entity_to_protobuf(entity):
    if isinstance(entity, Model):
      return model_to_protobuf(entity, project, namespace)

    return real_entity_to_protobuf(entity)

  if project:
    global DEFAULT_PROJECT_NAME
    DEFAULT_PROJECT_NAME = project

    # enable via monkey patching
    datastore.helpers.entity_from_protobuf = new_entity_from_protobuf
    datastore.helpers.entity_to_protobuf = new_entity_to_protobuf
  else:
    # disable: revert to orginal functions
    datastore.helpers.entity_from_protobuf = real_entity_from_protobuf
    datastore.helpers.entity_to_protobuf = real_entity_to_protobuf

class Key(DatastoreKey):

  def __init__(self, model_cls, *path_args, **kwargs):
    kwargs.setdefault('project', DEFAULT_PROJECT_NAME)
    super(self.__class__, self).__init__(
      model_cls._get_kind(),
      *path_args,
      **kwargs
    )
