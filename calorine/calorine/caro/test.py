
import os
import sys
import hashlib

from PIL import Image
from requests import get
from StringIO import StringIO
import memcache

mmc = memcache.Client(['127.0.0.1:11211'], debug=0)

url = 'http://l1.yimg.com/nn/fp/rsz/121912/images/smush/rama_1355927347.jpg'

key = 'toto'

raw = get(url, timeout=5)


img = Image.open(StringIO(raw.content))

mmc.set("%s_data" % key, img.tostring())
mmc.set("%s_mode" % key, img.mode)
mmc.set("%s_size" % key, img.size)



size = mmc.get("%s_size" % key)
mode = mmc.get("%s_mode" % key)
data = mmc.get("%s_data" % key)


print mode

amg = Image.fromstring(mode, size, data)
amg.save('/tmp/foo.jpg')
