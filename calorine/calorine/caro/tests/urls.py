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
Unit tests for urls in caro

"""
from django.contrib.auth.models import User
from django.test import TestCase, Client


class UrlsTests(TestCase):  # pylint: disable-msg=R0904
    """
    The url view

    """
    def setUp(self):
        """
        Init
        """
        self.user = User.objects.create_user('admin_search',
                                             'admin_search@bar.com',
                                             'admintest')

    def test_history(self):
        """
        History url
        """
        client = Client()
        client.login(username='admin_search', password='admintest')
        response = client.get('/history/')
        self.assertContains(response, self.user.username, status_code=200)

    def test_songs(self):
        """
        Songs url
        """
        client = Client()
        client.login(username='admin_search', password='admintest')
        response = client.get('/songs/')
        self.assertContains(response, self.user.username, status_code=200)

    def test_main(self):
        """
        Songs url
        """
        client = Client()
        client.login(username='admin_search', password='admintest')
        response = client.get('/')
        self.assertContains(response, self.user.username, status_code=200)

    def test_logs(self):
        """
        History url
        """
        client = Client()
        client.login(username='admin_search', password='admintest')
        response = client.get('/logs/')
        self.assertContains(response, self.user.username, status_code=200)
