# -*- coding: utf-8 -*-
"""

 Copyright (c) 2012 Rodolphe Quiédeville <rodolphe@quiedeville.org>

     This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     You should have received a copy of the GNU General Public License
     along with this program.  If not, see <http://www.gnu.org/licenses/>.

 Context processors definition

"""
from django.core.cache import cache


def onair(request):
    """Retrieve datas from cache
    """
    key_full = 'onair_full'
    full = ''
    if cache.get(key_full):
        full = cache.get(key_full)

    return {'ONAIR_FULL': full}


def searchq(request):
    """
    The search string
    """
    qry_str = request.GET.get('q')

    return {'SEARCHQ': qry_str}
