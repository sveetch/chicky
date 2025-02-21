import argparse
from pathlib import Path

from tabulate import tabulate

from chicky.cli.entrypoint import argumentparser_init


class DocumentationCommandParser:
    """
    Dummy 'argparse' parser to collect argument informations.
    """
    HELP_ARG = {
        "names": "``--help``",
        "type": "flag",
        "metavar": None,
        "help": "Display help message and exit"
    }


    def __init__(self, *args, **kwargs):
        self.arguments = []

    def add_argument(self, *args, **kwargs):
        """
        Simulate ``Parser.add_argument`` to receive argument options and
        store them into ``DocumentationCommandParser.arguments`` dictionnary. Option
        contents will contain some RST syntax.
        """
        type_display = "str"
        if kwargs.get("type"):
            type_display = kwargs.get("type").__name__
        else:
            if kwargs.get("action", "") in ("store_true", "store_false"):
                type_display = "bool"

        argnames = ["``{}``".format(k) for k in args]

        self.arguments.append({
            "names": " / ".join(argnames),
            "type": type_display,
            "metavar": kwargs.get("metavar"),
            "help": kwargs.get("help"),
        })

    def get_documentation_as_table(self):
        """
        Format collected arguments to a RST table with tabulate library.
        """
        if self.HELP_ARG:
            self.arguments.append(self.HELP_ARG)

        table = tabulate(
            [
                [arg_doc["names"], arg_doc["type"], arg_doc["help"]]
                for arg_doc in self.arguments
            ],
            tablefmt="grid",
            headers=["Option", "Type", "Help"],
        )
        return str(table)

    def get_arguments_documentation_as_deflist(self):
        """
        Format collected arguments to a RST definition list.
        """
        if self.HELP_ARG:
            self.arguments.append(self.HELP_ARG)

        output = []
        for arg_doc in self.arguments:
            output.append("{} *({})*".format(arg_doc["names"], arg_doc["type"]))
            output.append("    " + arg_doc["help"])
            output.append("")

        return "\n".join(output)


def make_command_documentation(destination_path):
    """
    Read command parser argument definitions to build a RST table and write it into a
    file.
    """
    parser = argumentparser_init(DocumentationCommandParser)
    doc = parser.get_arguments_documentation_as_deflist()
    destination_path.write_text(doc)
    print("  └── Command documentation has been written to:", destination_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Create ReStructuredText table of a command arguments"
        ),
    )
    parser.add_argument(
        "destination",
        type=Path,
        default=None,
        metavar="FILEPATH",
        help=(
            "Filepath where to write content. Existing file will be overwritten."
        )
    )

    args = parser.parse_args()

    make_command_documentation(args.destination)
