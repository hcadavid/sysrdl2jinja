import sys
import os
import json

from systemrdl import RDLCompiler, RDLCompileError, RDLWalker
from RDLModelListeners import MyModelPrintingListener

# Collect input files from the command line arguments
input_files = sys.argv[1:]

# Create an instance of the compiler
rdlc = RDLCompiler()


try:
    # Compile all the files provided
    for input_file in input_files:
        rdlc.compile_file(input_file)

    # Elaborate the design
    root = rdlc.elaborate()
    # Traverse the register model!

    registers = []

    #iterate over registries definition
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

        registers.append(register)

    print(registers)

    #walker = RDLWalker(unroll=True)
    #listener = MyModelPrintingListener()
    #walker.walk(root, listener)


except RDLCompileError:
    # A compilation error occurred. Exit with error code
    sys.exit(1)

