"""

"""
import hashlib

def hashfile(filepath):
    """
    Calculate the sha1 value of a file
    """
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()
