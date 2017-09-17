# -*- encoding: utf-8 -*-
# vim: sts=2:ts=2:sw=2

# TODO python 2 compat (2L ** 63)
_MAX_LONG = 2 ** 63  # Use 2L, see issue 65.  http://goo.gl/ELczz
# _MAX_KEYPART_BYTES = 500

class Key(object):
  def __init__(self, *_args, **_kwargs):
    raise NotImplementedError('Key class is not set up (yet)')
