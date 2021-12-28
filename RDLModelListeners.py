from systemrdl import RDLListener
from systemrdl.node import FieldNode


# Define a listener that will print out the register model hierarchy
class MyModelPrintingListener(RDLListener):
    def __init__(self):
        self.indent = 0

    def enter_Component(self, node):
        if not isinstance(node, FieldNode):
            print("C\t" * self.indent, node.get_path_segment())
            self.indent += 1

    def enter_Field(self, node):
        # Print some stuff about the field
        bit_range_str = "[%d:%d]" % (node.high, node.low)
        sw_access_str = "sw=%s" % node.get_property("sw").name
        print("F\t" * self.indent, bit_range_str, node.get_path_segment(), sw_access_str)

    def exit_Component(self, node):
        if not isinstance(node, FieldNode):
            self.indent -= 1
