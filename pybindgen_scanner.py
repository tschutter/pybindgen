#!/usr/bin/env python

"""
Generates pybindgen binding code from a C/C++ header file.

Requires python-pygccxml package.
"""

import optparse
import re
import sys

sys.path.append("pybindgen-0.15.0.zip/pybindgen-0.15.0")
import pybindgen
import pybindgen.gccxmlparser


def main():
    """main"""
    # Define options.
    option_parser = optparse.OptionParser(
        usage="usage: %prog [options] HEADERFILE ...\n"
            "  Generates Python binding code from C/C++ header files."
    )
    option_parser.add_option(
        "-I",
        action="append",
        dest="include_paths",
        metavar="DIR",
        default=[],
        help="add the directory DIR to the list of include directories"
    )
    option_parser.add_option(
        "-D",
        action="append",
        dest="define_symbols_raw",
        metavar="NAME=DEF",
        default=[],
        help="predefine NAME as a macro with definition DEF"
    )
    option_parser.add_option(
        "--name",
        action="store",
        dest="name",
        metavar="NAME",
        help="output Python module name"
    )

    # Parse and check options.
    (options, args) = option_parser.parse_args()
    if options.name == None:
        option_parser.error("--name not specified")
    if len(args) == 0:
        option_parser.error("HEADERFILE not specified")
    options.define_symbols = dict()
    for raw in options.define_symbols_raw:
        name_def = raw.split("=", 1)
        if len(name_def) == 1:
            name_def.append("1")
        options.define_symbols[name_def[0]] = name_def[1]

    ofilename = options.name + "_gen.py"
    with open(ofilename, "w") as ofile:
        module_parser = pybindgen.gccxmlparser.ModuleParser(options.name)
        module_parser.parse(
            header_files=args,
            whitelist_paths=options.include_paths,
            pygen_sink=pybindgen.FileCodeSink(ofile),
            gccxml_options=dict(
                include_paths=options.include_paths,
                define_symbols=options.define_symbols
            )
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
