#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase, main

import binascii
import ndb_orm as ndb
from google.cloud.proto.datastore.v1 import entity_pb2

class Person(ndb.Model):
    name = ndb.TextProperty(indexed=False, compressed=True)

class ProotocollBuffer(TestCase):

    def test_from_stringified(self):

        # hexlified protocolbuffer of Person(name='Hallo')
        pb_binary_string = binascii.unhexlify("0a250a10120e616161616161616161616161616112110a06506572736f6e10808080808080800a1a1d0a046e616d651215701692010d789cf348ccc9c90700057c01f1980101")

        pb = entity_pb2.Entity()
        pb.ParseFromString(pb_binary_string)
        model = ndb.model_from_pb(pb)

        self.assertEqual(model._class_name(), "Person")
        self.assertEqual(model.name, "Hallo")

if __name__ == '__main__':
    main()
