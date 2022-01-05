import sys
import os
from systemrdl.parser.sa_systemrdl import SA_ErrorListener
from systemrdl import preprocessor
from systemrdl.parser import sa_systemrdl
import print_tree
import sys
import base64
import zlib
import print_tree
from print_tree import OtherTraverseListener
from systemrdl import RDLListener
from systemrdl.node import FieldNode, Node
from systemrdl import RDLCompiler, RDLCompileError, RDLWalker
from systemrdl.parser import sa_systemrdl
from systemrdl import preprocessor
from systemrdl.parser.sa_systemrdl import SA_ErrorListener
from antlr4 import InputStream, Token


class __DetailedSyntaxErrorListener(SA_ErrorListener):

    def __init__(self):
        self.syntax_error_details = None
        self.count = 0

    def syntaxError(self, input_stream: InputStream, offending_symbol: Token, char_index: int, line: int, column: int,
                    msg: str):
        self.syntax_error_details = RDLSyntaxError(offending_symbol, char_index, line, column, msg)


def __get_detailed_syntax_error(rdl_file_path):
    rdlc2 = RDLCompiler()
    input_stream = preprocessor.preprocess_file(rdlc2.env, rdl_file_path, [])
    se_listener = __DetailedSyntaxErrorListener()
    parsed_tree = sa_systemrdl.parse(
        input_stream,
        "root",
        se_listener
    )
    return se_listener.syntax_error_details


def parse_rdl_file(rdl_file):
    # Create an instance of the compiler
    rdlc = RDLCompiler()

    rdlc.compile_file(rdl_file)

    # Elaborate the design
    root = rdlc.elaborate()

    registers = []

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

    registers.append(register)
    return registers


if __name__ == "__main__":
    from systemrdl import RDLCompiler, RDLCompileError, RDLWalker
    from RDLModelListeners import MyModelPrintingListener
    from jinja2 import Template

    # Collect input files from the command line arguments
    rdl_file = sys.argv[1]

    try:
        registers = parse_rdl_file(rdl_file)
        print(registers)
    except RDLCompileError as exc:
        # the document is parsed again with a custom listener to get the details of the syntax error
        # this is done due to a limitation of the RDLCompiler API
        detailed_se = __get_detailed_syntax_error(rdl_file)
        print(detailed_se)
