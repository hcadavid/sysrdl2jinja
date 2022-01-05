import sys
import os


def parse_rdl_file(_rdl_file):
    # Create an instance of the compiler
    rdlc = RDLCompiler()

    rdlc.compile_file(_rdl_file)

    # Elaborate the design
    root = rdlc.elaborate()

    _registers = []

    # iterate over registries definition
    for register_def in root.top.inst.children:
        register = dict()
        register["name"] = register_def.inst_name
        fields = []
        register["fields"] = fields

        for field_def in register_def.children:
            field = dict()
            field["id"] = field_def.inst_name
            field["low"] = field_def.low
            field["lsb"] = field_def.lsb
            field["msb"] = field_def.msb
            field["width"] = field_def.width
            if "hw" in field_def.properties:
                field["rights"] = field_def.properties["hw"].value
            else:
                field["rights"] = "undefined"
            if "reset" in field_def.properties:
                field["reset"] = field_def.properties["reset"]
            else:
                field["reset"] = "undefined"
            fields.append(field)

    _registers.append(register)
    return _registers


if __name__ == "__main__":
    from systemrdl import RDLCompiler, RDLCompileError, RDLWalker
    from RDLModelListeners import MyModelPrintingListener
    from jinja2 import Template

    # Collect input files from the command line arguments
    rdl_file = sys.argv[1]

    try:
        registers = parse_rdl_file(rdl_file)
        print(registers)
        exit(0)
    except RDLCompileError as exc:
        # error details are sent to stderr by the parser, next line add further details
        print("File: ", rdl_file, file=sys.stderr)
        exit(1)
        