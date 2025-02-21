.. _overview_intro:

========
Overview
========

Efficiency
**********

Chicky try to be efficient as possible and you should be safe to use it on hundreds of
files with an average size.

Above this measures, you should care about amount of files you are traversing, file
size can be a concern when they are larger than 500Mb but the most important is the
amount of files to process.

Don't forget to use filter options to limit file traversing that you don't need.


Checksum algorithm
******************

We chosen Blake2b algorithm because it is efficient and naturally support hash digest
size.

It is widely deployed on distributions with the `GNU Core Utilities <https://www.gnu.org/software/coreutils/>`_
which provides a command ``b2sum`` that you may use for comparaison (`BLAKE2 checksum <https://www.gnu.org/savannah-checkouts/gnu/coreutils/manual/html_node/b2sum-invocation.html>`_)
for a file: ::

    b2sum yourdownloadedfile.tar.gz

Formats
*******

On default the output of Chicky is in JSON: ::

    {
        "created": "2025-01-15T10:00:00",
        "basedir": "mydirectory",
        "extensions": None,
        "files": {
            "empty.txt": "3345524abf6bbe1809449224b5972c41790b6cf2",
            "css/bootstrap.css": "b5b31416eb16e75e8d35469467229af5954d7ebf",
        }
    }

You may however prefer a more basic text format with the option ``--format text``: ::

    file.txt   3345524abf6bbe1809449224b5972c41790b6cf2
    css/bootstrap.css   b5b31416eb16e75e8d35469467229af5954d7ebf

From this format the columns are divided with a tabulation character.

Filtering
*********

You have some optional command argument to apply basic filtering on file collection.

As an advanced example with this structure: ::

    sample
    ├── css
    │   ├── bootstrap.css
    │   ├── parts
    │   │   ├── bootstrap-grid.css
    │   │   └── bootstrap-reboot.css
    │   └── vendor
    │       └── bootstrap-icons.css
    ├── empty.txt
    └── images
        ├── atoum
        │   ├── favicon.ico
        │   └── logo.png
        ├── favicon.ico
        ├── furo-adjustments.css
        ├── logo.png
        └── lotus
            ├── favicon.ico
            └── logo.png

With the following command: ::

    chicky --format=text --ext=css --ignore-dir-lead=images --ignore-dir-lead=css/vendor \
        --ignore-file-lead=bootstrap- --ignore-file-lead=logo.p sample

Here we applied filters:

* Only files ending with ``.css`` extension are collected;
* Paths with a directory starting with ``images`` are not collected;
* Paths with a directory starting with ``css/vendor`` are not collected;
* Paths with a filename starting with ``bootstrap-`` are not collected;
* Paths with a filename starting with ``logo.p`` are not collected;

.. Note::
    Filters from ``--ignore-dir-lead`` and ``--ignore-file-lead`` are matched again the
    relative path, it means relatively to the source directory path.

We used text format (to ease readability) and so you would get the following output: ::

    css/bootstrap.css    b5b31416eb16e75e8d35469467229af5954d7ebf
