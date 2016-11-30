# Copyright (c) 2013 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import unittest

from oslo_utils import uuidutils

from openstack_dashboard.utils import config_types
from openstack_dashboard.utils import filters


class UtilsFilterTests(unittest.TestCase):
    def test_accept_valid_integer(self):
        val = 100
        ret = filters.get_int_or_uuid(val)
        self.assertEqual(val, ret)

    def test_accept_valid_integer_string(self):
        val = '100'
        ret = filters.get_int_or_uuid(val)
        self.assertEqual(int(val), ret)

    def test_accept_valid_uuid(self):
        val = uuidutils.generate_uuid()
        ret = filters.get_int_or_uuid(val)
        self.assertEqual(val, ret)

    def test_reject_random_string(self):
        val = '55WbJTpJDf'
        self.assertRaises(ValueError, filters.get_int_or_uuid, val)


class ConfigTypesTest(unittest.TestCase):
    def test_literal(self):
        literal = config_types.Literal([0])
        self.assertEqual([1, 2, 3], literal("[1, 2, 3]"))
        self.assertRaises(ValueError, literal, "[1, '2', 3]")

        literal = config_types.Literal({0: ""})
        self.assertEqual({1: 'a', 2: u'b'}, literal("{1: 'a', 2: u'b'}"))
        self.assertRaises(ValueError, literal, "[1, '2', 3]")
        self.assertRaises(ValueError, literal, "{1: 1, '2': 2}")

        literal = config_types.Literal((True, 1, ""))
        self.assertEqual((True, 13, 'x'), literal("(True, 13, 'x')"))
        self.assertRaises(ValueError, literal, "(True, True)")
        self.assertRaises(ValueError, literal, "(True, True, False, False)")
        self.assertRaises(ValueError, literal, "(2, True, 'a')")
        self.assertRaises(ValueError, literal, "(")

        literal = config_types.Literal([(True, 1, lambda s: s.upper())])
        self.assertEqual([(True, 13, 'X')], literal("[(True, 13, 'x')]"))

    def test_url(self):
        url = config_types.URL()
        self.assertEqual('/webroot/static/', url('/webroot//static'))
        self.assertEqual('http://webroot/static/',
                         url('http://webroot//static'))
