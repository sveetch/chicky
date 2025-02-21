import os
from hashlib import blake2b
from pathlib import Path


def checksum(filepath, digest_size=20):
    """
    Checksum a file in an efficient way for large files with blake2b.

    Borrowed from: https://stackoverflow.com/a/44873382

    .. Todo::
        Once minimal Python version support move to 3.11 we should be able to simplify
        this code with ``hashlib.file_digest()`` usage instead.

    Arguments:
        filepath (pathlib.Path): File path to open and checksum.

    Keyword Arguments:
        digest_size (integer): Maximum size of hash digest. This is the size of hash in
            bytes, the returned string will be longer since it is the hexadecimal
            digest. Commonly if you want a string of 10 characters you should ask for a
            digest of ``20``.

    Returns:
        string: The file checksum.
    """
    h = blake2b(digest_size=digest_size)
    b = bytearray(128 * 1024)
    mv = memoryview(b)

    with open(filepath, "rb", buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])

    return h.hexdigest()


def collect_files(dirpath, extensions=None, dir_leads=None, filename_leads=None):
    """
    Recursively collect every file from a directory and compute their checksum.

    Arguments:
        dirpath (string or pathlib.Path):

    Keyword Arguments:
        extensions (list): List of allowed file extensions. When it is not empty, each
            that does not match any of those extensions will be ignored.
        dir_leads (list): A list of leading patterns to check on paths, each
            path starting with one of those patterns will be ignored. Match is performed
            against the relative file path (from the ``dirpath``).
        filename_leads (list): A list of leading patterns to check on filenames,
            each filename starting with one of those patterns will be ignored.

    Returns:
        Generator: Yield tuples of path + checksum string
    """
    extensions = tuple("." + v for v in extensions) if extensions else None
    dir_leads = tuple(dir_leads) if dir_leads else None
    filename_leads = tuple(filename_leads) if filename_leads else None

    for root, dirs, files in os.walk(dirpath):
        for item in files:
            rel = os.path.relpath(root, start=dirpath)
            # Only collect item that pass filters
            if (
                (not dir_leads or not rel.startswith(dir_leads)) and
                (not filename_leads or not item.startswith(filename_leads)) and
                (not extensions or item.endswith(extensions))
            ):
                path = Path(os.path.join(root, item))
                yield (path.relative_to(dirpath), checksum(path))
