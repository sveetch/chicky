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

from ..core import ExtendedJsonEncoder, collect_files


def main(argv=sys.argv):
    parser = argparse.ArgumentParser(
        description=(
            "Build a Blake2b hash for every files recursively from a directory and "
            "store them into a manifest file."
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
            "Allowed extensions. Only filenames ending with one allowed extensions "
            "will be collected. You can use it multiple times to allow multiple "
            "extension. If no extension is given then all files are collected. Do not "
            "start your extension pattern with their leading dot because it is already "
            "appended from code."
        )
    )
    parser.add_argument(
        "--destination",
        metavar="FILE_PATH",
        type=Path,
        help="Path where to write file of collected files and their checksum.",
    )
    parser.add_argument(
        "--format",
        default="json",
        choices=["json", "text"],
        help="Output format. JSON format is the one with the most informations.",
    )

    args = parser.parse_args(argv[1:])

    files = collect_files(args.source, extensions=args.ext)

    # Serialize to format
    if args.format == "text":
        manifest = "\n".join([
            str(path) + "\t" + checksum
            for path, checksum in files
        ])
    else:
        store = {
            "created": datetime.datetime.now().isoformat(timespec="seconds"),
            "basedir": args.source,
            "extensions": args.ext,
            "files": {
                str(path): checksum
                for path, checksum in files
            },
        }
        manifest = json.dumps(store, indent=4, cls=ExtendedJsonEncoder)

    if args.destination:
        args.destination.write_text(manifest)
    else:
        print(manifest)
