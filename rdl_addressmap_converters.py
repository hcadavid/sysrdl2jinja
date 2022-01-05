import print_tree
import sys
import base64
import zlib
import print_tree
from print_tree import OtherTraverseListener
from systemrdl import RDLListener
from systemrdl.node import FieldNode, Node
from systemrdl import RDLCompiler, RDLCompileError, RDLWalker
from rdl_parsing_exceptions import RDLTransformationException, RDLSyntaxRelatedTransformationException
from systemrdl.parser import sa_systemrdl
from systemrdl import preprocessor
from systemrdl.parser.sa_systemrdl import SA_ErrorListener
from antlr4 import InputStream, Token


class RDLSyntaxError:
    def __init__(self, offending_symbol: Token, char_index: int, line: int, column: int,
                 msg: str):
        self.offending_symbol = offending_symbol
        self.char_index = char_index
        self.line = line
        self.column = column
        self.msg = msg

    def __str__(self) -> str:
        return "Error on line %d, column %d: %s" % (self.line,
                                                    self.column,
                                                    self.msg)


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


def rdl_to_kroki_url(rdl_file_path):

    rdlc = RDLCompiler()

    try:
        rdlc.compile_file(rdl_file_path)
        root = rdlc.elaborate()
        # Traverse the register model
        walker = RDLWalker(unroll=True)
        # listener = MyModelPrintingListener()
        listener = OtherTraverseListener()
        walker.walk(root, listener)

        html_output = ''

        # TODO externalize/define RDL files encoding
        # TODO kroki API url as a parameter
        for rdl_register in listener.byte_field_reg_desc:
            encoded_diagram = base64.urlsafe_b64encode(zlib.compress(bytearray(rdl_register, 'UTF-8')))
            html_output += '<img src="https://kroki.io/bytefield/svg/%s">' % encoded_diagram.decode("UTF-8") + '\n'

        return html_output

    except RDLCompileError as exc:
        # the document is parsed again with a custom listener to get the details of the syntax error
        # this is done due to a limitation of the RDLCompiler API
        detailed_se = __get_detailed_syntax_error(rdl_file_path)

        if detailed_se is None:
            raise RDLTransformationException() from exc
        else:
            raise RDLSyntaxRelatedTransformationException(detailed_se) from exc



