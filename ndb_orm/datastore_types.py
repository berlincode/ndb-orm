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

# stripped down version of  google/appengine/api/datastore_types.py

from . import datastore_errors

_MAX_STRING_LENGTH = 500

def typename(obj):
  """Returns the type of obj as a string. More descriptive and specific than
  type(obj), and safe for any object, unlike __class__."""
  if hasattr(obj, '__class__'):
    return getattr(obj, '__class__').__name__
  else:
    return type(obj).__name__

def ValidateString(value,
                   name='unused',
                   exception=datastore_errors.BadValueError,
                   max_len=_MAX_STRING_LENGTH,
                   empty_ok=False):
  """Raises an exception if value is not a valid string or a subclass thereof.

  A string is valid if it's not empty, no more than _MAX_STRING_LENGTH bytes,
  and not a Blob. The exception type can be specified with the exception
  argument; it defaults to BadValueError.

  Args:
    value: the value to validate.
    name: the name of this value; used in the exception message.
    exception: the type of exception to raise.
    max_len: the maximum allowed length, in bytes.
    empty_ok: allow empty value.
  """
  if value is None and empty_ok:
    return
  if not isinstance(value, str):
    raise exception('%s should be a string; received %s (a %s):' %
                    (name, value, typename(value)))
  if not value and not empty_ok:
    raise exception('%s must not be empty.' % name)

  if len(value.encode('utf-8')) > max_len:
    raise exception('%s must be under %d bytes.' % (name, max_len))


class GeoPt(object):
  """A geographical point, specified by floating-point latitude and longitude
  coordinates. Often used to integrate with mapping sites like Google Maps.
  May also be used as ICBM coordinates.

  This is the georss:point element. In XML output, the coordinates are
  provided as the lat and lon attributes. See: http://georss.org/

  Serializes to '<lat>,<lon>'. Raises BadValueError if it's passed an invalid
  serialized string, or if lat and lon are not valid floating points in the
  ranges [-90, 90] and [-180, 180], respectively.
  """
  lat = None
  lon = None

  def __init__(self, lat, lon=None):
    if lon is None:

      try:
        split = lat.split(',')
        lat, lon = split
      except (AttributeError, ValueError):
        raise datastore_errors.BadValueError(
          'Expected a "lat,long" formatted string; received %s (a %s).' %
          (lat, typename(lat)))

    try:
      lat = float(lat)
      lon = float(lon)
      if abs(lat) > 90:
        raise datastore_errors.BadValueError(
          'Latitude must be between -90 and 90; received %f' % lat)
      if abs(lon) > 180:
        raise datastore_errors.BadValueError(
          'Longitude must be between -180 and 180; received %f' % lon)
    except (TypeError, ValueError):

      raise datastore_errors.BadValueError(
        'Expected floats for lat and long; received %s (a %s) and %s (a %s).' %
        (lat, typename(lat), lon, typename(lon)))

    self.lat = lat
    self.lon = lon

  def __cmp__(self, other):
    if not isinstance(other, GeoPt):
      try:
        other = GeoPt(other)
      except datastore_errors.BadValueError:
        return NotImplemented


    lat_cmp = cmp(self.lat, other.lat)
    if lat_cmp != 0:
      return lat_cmp
    else:
      return cmp(self.lon, other.lon)

  def __hash__(self):
    """Returns an integer hash of this point.

    Implements Python's hash protocol so that GeoPts may be used in sets and
    as dictionary keys.

    Returns:
      int
    """
    return hash((self.lat, self.lon))

  def __repr__(self):
    """Returns an eval()able string representation of this GeoPt.

    The returned string is of the form 'datastore_types.GeoPt([lat], [lon])'.

    Returns:
      string
    """
    return 'datastore_types.GeoPt(%r, %r)' % (self.lat, self.lon)

  def __unicode__(self):
    return '%s,%s' % (str(self.lat), str(self.lon))

  __str__ = __unicode__

  def ToXml(self):
    return '<georss:point>%s %s</georss:point>' % (str(self.lat),
                                                    str(self.lon))

class BlobKey(object):
  """Key used to identify a blob in Blobstore.

  This object wraps a string that gets used internally by the Blobstore API
  to identify application blobs.  The BlobKey corresponds to the entity name
  of the underlying BlobReference entity.

  This class is exposed in the API in both google.appengine.ext.db and
  google.appengine.ext.blobstore.
  """

  def __init__(self, blob_key):
    """Constructor.

    Used to convert a string to a BlobKey.  Normally used internally by
    Blobstore API.

    Args:
      blob_key:  Key name of BlobReference that this key belongs to.
    """
    ValidateString(blob_key, 'blob-key')
    self.__blob_key = blob_key

  def __str__(self):
    """Convert to string."""
    return self.__blob_key

  def __repr__(self):
    """Returns an eval()able string representation of this key.

    Returns a Python string of the form 'datastore_types.BlobKey(...)'
    that can be used to recreate this key.

    Returns:
      string
    """
    return 'datastore_types.%s(%r)' % (type(self).__name__, self.__blob_key)

  def __cmp__(self, other):


    if type(other) is type(self):
      return cmp(str(self), str(other))
    elif isinstance(other, str):
      return cmp(self.__blob_key, other)
    else:
      return NotImplemented

  def __hash__(self):
    return hash(self.__blob_key)
