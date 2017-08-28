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

"""NDB -- A new datastore API for the Google App Engine Python runtime."""

__version__ = '0.1.0' # originally based on ndb '1.0.10'

from google.cloud import datastore

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


DEFAULT_MODEL = None

def model_from_pb(pb):
    if not pb.HasField('key'):  # Message field (Key)
        return None

    key = datastore.helpers.key_from_protobuf(pb.key)
    try:
        modelclass = Model._lookup_model(key.kind, DEFAULT_MODEL)
    except KindError:
        return None
    key = None
    entity = modelclass._from_pb(pb, key=key, set_key=False)
    return entity

def model_to_pb(client, entity_of_ndb_model):
    entity_of_ndb_model._prepare_for_put()
    pb = entity_of_ndb_model._to_pb()

    if entity_of_ndb_model._key is None:
        entity_of_ndb_model._key = client.key(entity_of_ndb_model.__class__.__name__)

    entity_of_ndb_model._pre_put_hook()
    key_pb = entity_of_ndb_model._key.to_protobuf()
    pb.key.CopyFrom(key_pb)
    return pb
