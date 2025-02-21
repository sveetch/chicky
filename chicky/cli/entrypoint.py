"""
Command line interface

.. todo::
    TODO: Need a '--version' just to display package version then exit.
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

from .. import __pkgname__, __version__
from ..core import collect_files


def argumentparser_init(parser_class):
    parser = parser_class(
        description=(
            "Build a Blake2b hash for every files recursively collected from a "
            "directory. "
            "({}=={})".format(__pkgname__, __version__)
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "source",
        type=Path,
        metavar="DIRECTORY_PATH",
        help=(
            "An existing path of a directory to traverse to find elligible files. "
            "Eligibility is defined from allowed extensions."
        )
    )
    parser.add_argument(
        "--ext",
        metavar="FILE_EXTENSION",
        action="append",
        help=(
            "This is for allowed file extensions. Only filenames ending with one of "
            "allowed extensions will be collected. You can use it multiple times to "
            "allow multiple extensions. If no extension is given then all files are "
            "collected. Do not start your extension pattern with their leading dot "
            "because it is already appended from code."
        )
    )
    parser.add_argument(
        "--ignore-dir-lead",
        metavar="PATTERN",
        action="append",
        help=(
            "This is a leading pattern that will exclude paths starting with it. This "
            "is applied on the relative (to the 'source' path) directory path. Use it "
            "multiple time to define multiple pattern, a single match exclude a path."
        )
    )
    parser.add_argument(
        "--ignore-file-lead",
        metavar="PATTERN",
        action="append",
        help=(
            "This is a leading pattern that will exclude files starting with it. This "
            "is applied on filename path. Use it multiple time to define multiple "
            "pattern, a single match exclude a path."
        )
    )
    parser.add_argument(
        "--destination",
        metavar="FILE_PATH",
        type=Path,
        help=(
            "This is the path where to write file of collected files and their "
            "checksum. If it is not given the data will be printed to standard output."
        ),
    )
    parser.add_argument(
        "--format",
        default="json",
        choices=["json", "text"],
        help=(
            "This is the format to serialize data. JSON format is the one with the "
            "most informations."
        ),
    )

    return parser


def main(argv=sys.argv):
    parser = argumentparser_init(argparse.ArgumentParser)
    args = parser.parse_args(argv[1:])

    files = collect_files(
        args.source,
        extensions=args.ext,
        dir_leads=args.ignore_dir_lead,
        filename_leads=args.ignore_file_lead,
    )

    # Serialize to format
    # TODO: Move to a function for formatting
    if args.format == "text":
        manifest = "\n".join([
            str(path) + "\t" + checksum
            for path, checksum in files
        ])
    else:
        store = {
            "created": datetime.datetime.now().isoformat(timespec="seconds"),
            "basedir": str(args.source),
            "extensions": args.ext,
            "files": {
                str(path): checksum
                for path, checksum in files
            },
        }
        manifest = json.dumps(store, indent=4)

    if args.destination:
        args.destination.write_text(manifest)
        print("Written output to: {}".format(args.destination))
    else:
        print(manifest)
