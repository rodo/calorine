# -*- coding: utf-8 -*-  pylint: disable-msg=R0801
#
# Copyright (c) 2012 Yohann Gabory <yohann@gabory.fr>
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
import requests
import json
from django.conf import settings

format = "json"

params = {"api_key": settings.LASTFM_API_KEY,
          "format": format}


def get_similar(artist, endpoint=settings.LASTFM_ENDPOINT):
    params['method'] = "artist.getSimilar"
    params['artist'] = artist
    resp = json.loads(requests.get(endpoint, params=params).content)
    response = []
    for elem in resp['similarartists']['artist']:
        response.append(elem['name'])
    return response


def get_tags(artist, track, endpoint=settings.LASTFM_ENDPOINT):
    params['method'] = "track.getInfo"
    params['artist'] = artist
    params['track'] = track
    resp = json.loads(requests.get(endpoint, params=params).content)
    response = []
    try:
        for elem in resp['track']['toptags']['tag']:
            response.append(elem['name'])
        return response
    except:
        return


def get_picture(artist, track, size="small", endpoint=settings.LASTFM_ENDPOINT):
    params['method'] = "track.getInfo"
    params['artist'] = artist
    params['track'] = track
    resp = json.loads(requests.get(endpoint, params=params).content)
    try:
        image = resp['track']['album']['image']
        for img in image:
            if img['size'] == size:
                return img['#text']
    except:
        return None

if __name__ == "__main__":
    print get_similar("Cher")
    print get_tags("Santa Esmeralda", "Don't Let Me Be Misunderstood")
