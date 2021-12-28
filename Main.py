import sys
import os

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
    walker = RDLWalker(unroll=True)
    listener = MyModelPrintingListener()
    walker.walk(root, listener)


except RDLCompileError:
    # A compilation error occurred. Exit with error code
    sys.exit(1)

