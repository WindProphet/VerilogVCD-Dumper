'Verilog VCD Dumper'
from . import dumper
from . import parser
from . import tikz

VerilogVCD = parser.VerilogVCD
VCDDumper = dumper.VCDDumper
# pylint: disable=C0103
apply = dumper.VCDDumper.from_setting
