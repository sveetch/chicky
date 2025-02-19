import json
import os
import types
from hashlib import blake2b
from pathlib import Path


class ExtendedJsonEncoder(json.JSONEncoder):
    """
    Additional opinionated support for more basic object types.

    Usage sample: ::

        json.dumps(..., cls=ExtendedJsonEncoder)
    """
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        # Support for pathlib.Path to a string
        if isinstance(obj, Path):
            return str(obj)
        if isinstance(obj, types.GeneratorType):
            return list(obj)

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def checksum(filepath):
    """
    Checksum a file in an efficient way for large files with blake2b.

    Borrowed from: https://stackoverflow.com/a/44873382

    Arguments:
        filepath (pathlib.Path): File path to open and checksum.

    Returns:
        string: The file checksum as 20 characters.
    """
    h = blake2b(digest_size=20)
    b = bytearray(128 * 1024)
    mv = memoryview(b)

    with open(filepath, "rb", buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])

    return h.hexdigest()


def collect_files(dirpath, extensions=None):
    """
    Build store for all files from a single base directory
    """
    extensions = tuple("." + v for v in extensions) if extensions else None

    for root, dirs, files in os.walk(dirpath):
        for item in files:
            if (not extensions or item.endswith(extensions)):
                path = Path(os.path.join(root, item))
                yield (path.relative_to(dirpath), checksum(path))
