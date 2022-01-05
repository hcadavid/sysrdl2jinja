import sys
import os
from systemrdl import RDLCompiler, RDLCompileError, RDLWalker
from jinja2 import Template


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
            field["high"] = field_def.high
            field["lsb"] = field_def.lsb
            field["msb"] = field_def.msb
            field["width"] = field_def.width
            if "name" in field_def.properties:
                field["name"] = field_def.properties["name"]
            else:
                field["name"] = "undefined"
            if "hw" in field_def.properties:
                field["rights"] = field_def.properties["hw"]
            else:
                field["rights"] = "undefined"
            if "reset" in field_def.properties:
                field["reset"] = field_def.properties["reset"]
            else:
                field["reset"] = "undefined"
            fields.append(field)

        _registers.append(register)

    return _registers


def main():

    if len(sys.argv) < 4:
        print("SystemRDL to Jinja template converter", file=sys.stderr)
        print("Syntax: ", sys.argv[0], " [rdl_file] [jinja_template_file] [output_file]", file=sys.stderr)
        exit(1)


    # Collect input files from the command line arguments
    rdl_file = sys.argv[1]
    template_file = sys.argv[2]
    output_file = sys.argv[3]

    try:
        registers = parse_rdl_file(rdl_file)
        with open(template_file) as file_:
            template = Template(file_.read())
        with open(output_file, 'w') as output_:
            output_.write(template.render(registers=registers))
        exit(0)
    except RDLCompileError as exc:
        # error details are sent to stderr by the parser, next line add further details
        print("File: ", rdl_file, file=sys.stderr)
        exit(1)
