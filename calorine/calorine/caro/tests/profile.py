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
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.test import TestCase, Client
from calorine.caro.models import Song


class ProfileTests(TestCase):  # pylint: disable-msg=R0904
    """
    The profile view

    """
    def setUp(self):
        """
        Init
        """
        self.site = Site.objects.create(domain='sample_site')
        self.user = User.objects.create_user('admin_search',
                                             'admin_search@bar.com',
                                             'admintest')
        settings.SITE_ID = 1

    def test_songs(self):
        """
        View profile
        """
        client = Client()
        client.login(username='admin_search', password='admintest')
        response = client.get('/accounts/profile/')
        self.assertContains(response, self.user.username, status_code=200)
