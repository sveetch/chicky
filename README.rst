.. _Python: https://www.python.org/

======
Chicky
======

Chicky is a tool to compute Blake2b checksums for files from a directory. It
will go recursively through the directory and collect every files that are elligibles.
Elligibility is determined from optional filters.

We tried to make it lightweight and efficient since it could be involved in continuous
integration pipelines.

Usage is simple: ::

    chicky mydirectory

That would output something like: ::

    {
        "created": "2025-01-15T10:00:00",
        "basedir": "mydirectory",
        "extensions": None,
        "files": {
            "empty.txt": "3345524abf6bbe1809449224b5972c41790b6cf2",
            "css/bootstrap.css": "b5b31416eb16e75e8d35469467229af5954d7ebf",
        }
    }

See documentation for more options and details.

Dependencies
************

The only dependency is `Python`_>=3.8 (currently tested on 3.8, 3.9, 3.10 and 3.11).

Links
*****

* Read the documentation on `Read the docs <https://chicky.readthedocs.io/>`_;
* Download its `PyPi package <https://pypi.python.org/pypi/chicky>`_;
* Clone it on its `Github repository <https://github.com/sveetch/chicky>`_;


Credits
*******

Logo vector and icon by `SVG Repo <https://www.svgrepo.com>`_.
