# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Rodolphe Quiédeville <rodolphe@quiedeville.org>
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
import song
import unittest
import utils

class UtilsTests(unittest.TestCase):  # pylint: disable-msg=R0904
    """
    The utils

    """
    def test_strdetag(self):
        """
        """
        datas = {'album': ['album'],
                 'artist': ['artist'],
                 'title': ['title']}

        result = utils.strdetag(datas)

        attend = "artist - title (album)"
        
        self.assertEqual(result, attend)

    def test_extract_command(self):
        """
        Extract command
        """
        result = utils.extract_command('toto: foo')
        self.assertEqual(result, 'foo')

        result = utils.extract_command('toto:   foo')
        self.assertEqual(result, 'foo')

        result = utils.extract_command('toto:foo')
        self.assertEqual(result, 'foo')

        result = utils.extract_command('toto:foo  ')
        self.assertEqual(result, 'foo')

        result = utils.extract_command('toto:   foo    ')
        self.assertEqual(result, 'foo')

        result = utils.extract_command('toto:   foo  toto  ')
        self.assertNotEqual(result, 'foo')


if __name__ == '__main__':
    unittest.main()
