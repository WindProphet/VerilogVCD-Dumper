from . import Parser

class VCDDumper():
    "Base class to handle VCD Dump Process"

    @staticmethod
    def fromSetting(setting, vcd = None):
        vcd = vcd or setting['file']
        if isinstance(vcd, Parser.VerilogVCD):
            vcd = Parser.VerilogVCD(vcd)


    def __init__(self, vcd):
        assert isinstance(vcd, Parser.VerilogVCD)
        self.vcd = vcd

    def init(self, parameter_list):
        raise NotImplementedError

    def timescale(self, parameter_list):
        raise NotImplementedError

    def signaline(self, parameter_list):
        raise NotImplementedError

    def dump(self, parameter_list):
        raise NotImplementedError
