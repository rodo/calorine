import requests
import json
api_key = "9cf47d9fa4689d0d50db43503a28e48f"
endpoint = "http://ws.audioscrobbler.com/2.0/"
format = "json"

params = {"api_key": api_key,
          "format": format}


def get_similar(artist):
    params['method'] = "artist.getSimilar"
    params['artist'] = artist
    resp = json.loads(requests.get(endpoint, params=params).content)
    response = []
    for elem in resp['similarartists']['artist']:
        response.append(elem['name'])
    return response


def get_tags(artist, track):
    params['method'] = "track.getInfo"
    params['artist'] = artist
    params['track'] = track
    resp = json.loads(requests.get(endpoint, params=params).content)
    response = []
    try:
        image = resp['track']['album']['image']
        for img in image:
            if img['size'] == "small":
                print img['#text']
        for elem in resp['track']['toptags']['tag']:
            response.append(elem['name'])
        return response
    except:
        return


def get_picture(artist, track, size="small"):
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
