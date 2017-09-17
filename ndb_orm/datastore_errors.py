# -*- encoding: utf-8 -*-
# vim: sts=2:ts=2:sw=2

#
# Copyright 2007 Google Inc.
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
#

# stripped down version of  google/appengine/api/datastore_errors.py

"""Errors used in the Python datastore API."""

# from .database_errors import (BadFilterError, BadValueError, BadArgumentError, Error)


class Error(Exception):
  """Base datastore error type.
  """

class BadValueError(Error):
  """Raised by Entity.__setitem__(), Query.__setitem__(), Get(), and others
  when a property value or filter value is invalid.
  """


class BadArgumentError(Error):
  """Raised by Query.Order(), Iterator.Next(), and others when they're
  passed an invalid argument.
  """

class BadFilterError(Error):
  """Raised by Query.__setitem__() and Query.Run() when a filter string is
  invalid.
  """
  def __init__(self, filter):
    self.filter = filter
    message = ('invalid filter: %s.' % self.filter).encode('utf-8')
    super(BadFilterError, self).__init__(message)
