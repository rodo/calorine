# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Rodolphe Quiédeville <rodolphe@quiedeville.org>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Unit tests for profil in caro

"""
from django.test import TestCase
from django.conf import settings
from calorine.caro.context_processors import onair
from calorine.caro.context_processors import searchq
import memcache


class ContextProcessorsTests(TestCase):  # pylint: disable-msg=R0904
    """
    The logs object

    """
    memc_addr = '127.0.0.1:11211'

    def SetUp(self):  # pylint: disable-msg=C0103
        """setUp the tests
        """
        mmb = 'django.core.cache.backends.memcached.MemcachedCache'
        settings.CACHES = {
            'default': {
                'BACKEND': mmb,
                'LOCATION': self.memc_addr,
                'KEY_PREFIX': 'calo_tests_'}}

    def test_onair(self):
        """
        Check that onair() return a dict containing right key
        """

        key = "onair_full"
        value = "mo0pabah4Quiuzeiw4mohnee"
        prefix = settings.CACHES['default']['KEY_PREFIX']

        mmc = memcache.Client([self.memc_addr], debug=0)
        mmc.set("%s:1:%s" % (prefix, key), value)

        results = onair(None)

        self.assertEqual(results['ONAIR_FULL'], value)

    def test_searchq(self):
        """
        Check that searchq() return a dict containing teh param 'q' present in
        request
        """

        from django.http import HttpRequest

        request = HttpRequest()
        request.GET = {'q': 'foobar'}

        results = searchq(request)

        self.assertEqual(results['SEARCHQ'], 'foobar')

    def test_searchq_empty(self):
        """
        Check that searchq() return a dict containing enempty string
        """

        from django.http import HttpRequest

        request = HttpRequest()
        request.GET = {}

        results = searchq(request)

        self.assertEqual(results['SEARCHQ'], None)
