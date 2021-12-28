from systemrdl import RDLListener
from systemrdl.node import FieldNode, Node


# (draw-column-headers {:labels (reverse column-labels)})

class OtherTraverseListener(RDLListener):
    byte_field_reg_desc = []


    def enter_Addrmap(self, node):
        bigendian = node.inst.properties.get('bigendian')
        littleendian = node.inst.properties.get('littleendian')


        # print("Entering addrmap", node.get_path())

    def exit_Addrmap(self, node):
        pass
        # print("Exiting addrmap", node.get_path())


    def enter_Reg(self, node):
        self.byte_field_reg_desc.append('(def boxes-per-row 16)(draw-column-headers)')

    def exit_Reg(self, node):
        pass

    def enter_Field(self, node):
        curr_reg_index = len(self.byte_field_reg_desc)-1

        field_size = node.width
        name = node.type_name

        node_txt = self.byte_field_reg_desc[curr_reg_index] + "\n" + "(draw-box \"%s\" {:span %d})" % (name, field_size)
        self.byte_field_reg_desc[curr_reg_index] = node_txt

    def exit_Field(self, node):
        print("Exiting field", node.get_path())


# Define a listener that will print out the register model hierarchy
class MyModelPrintingListener(RDLListener):
    def __init__(self):
        self.indent = 0

    def enter_Component(self, node):
        if not isinstance(node, FieldNode):
            print("\t" * self.indent, node.get_path_segment())
            self.indent += 1

    def enter_Field(self, node):
        # Print some stuff about the field
        bit_range_str = "[%d:%d]" % (node.high, node.low)
        sw_access_str = "sw=%s" % node.get_property("sw").name
        print("\t" * self.indent, bit_range_str, node.get_path_segment(), sw_access_str)

    def exit_Component(self, node):
        if not isinstance(node, FieldNode):
            self.indent -= 1


if __name__ == "__main__":
    import sys
    import os

    from systemrdl import RDLCompiler, RDLCompileError, RDLWalker

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
    except RDLCompileError:
        # A compilation error occurred. Exit with error code
        sys.exit(1)

    #root.fields()
    # Traverse the register model!
    walker = RDLWalker(unroll=True)
    # listener = MyModelPrintingListener()
    listener = OtherTraverseListener()
    walker.walk(root, listener)
    print(listener.byte_field_reg_desc[0]);
    print(listener.byte_field_reg_desc[1]);
