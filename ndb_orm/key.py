# -*- encoding: utf-8 -*-
# vim: sts=2:ts=2:sw=2

import six

_MAX_LONG = 2 ** 63
# _MAX_KEYPART_BYTES = 500

DEFAULT_PROJECT_NAME = "<default-project-name>" #google.cloud.datastore does not allow empty project names - please initialize if you use keys

def set_default_project_name(project):
  global DEFAULT_PROJECT_NAME
  DEFAULT_PROJECT_NAME = project

def get_default_project_name():
  return DEFAULT_PROJECT_NAME

class KeyBase(object):
  def __init__(self, *_args, **_kwargs):
    raise NotImplementedError('KeyBase class is not set up (yet)')

  def get(self):
    raise NotImplementedError('KeyBase class is not set up (yet)')

  def delete(self):
    raise NotImplementedError('KeyBase class is not set up (yet)')

  @classmethod
  def from_legacy_urlsafe(_cls, _urlsafe):
    raise NotImplementedError('KeyBase class is not set up (yet)')

class KeyClass(object):

  def __call__(self, model_cls, *path_args, **kwargs):
    kwargs['project'] = kwargs.pop('project', None) or get_default_project_name()

    # accept model classes and plain strings as object instances
    if isinstance(model_cls, six.string_types):
      model_cls_str = model_cls
    else:
      model_cls_str = model_cls._get_kind()

    path_args = list(path_args)
    for i in range(1, len(path_args), 2):
      # accept both, plain strings and object instances as path
      if not isinstance(model_cls, six.string_types):
        path_args[i] = path_args[i]._get_kind()
    
    return KeyBase(
      model_cls_str,
      *path_args,
      **kwargs
    )

  @classmethod
  def from_legacy_urlsafe(cls, urlsafe):
    return KeyBase.from_legacy_urlsafe(urlsafe)

Key = KeyClass()
