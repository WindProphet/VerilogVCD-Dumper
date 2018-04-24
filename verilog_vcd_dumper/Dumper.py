"Dumper Base Class"
from . import parser


class VCDDumper():
    "Base class to handle VCD Dump Process"

    DumperFormaterList = {}
    DumperTypeDefault = 'tikz'

    @staticmethod
    def from_setting(setting, vcd=None):
        """Run Dumper use dict setting

        {
            'file': filename or `VerilogVCD`
            'setting': {
                'type': 'tikz' # dump formater: string or `VCDDumper`
                ..args
            },
            'timescale': {
                'start': '0ns',
                'end'  : '100ns',
                'major': '10ns',
                'minor': '2ns'
            },
            'signals': [
                {}
            ],
            'dump': {

            }
        }
        """
        vcd = vcd or setting['file']
        if not isinstance(vcd, parser.VerilogVCD):
            vcd = parser.VerilogVCD(vcd)
        if 'setting' in setting and 'type' in setting['setting']:
            instance = VCDDumper.DumperFormaterList[setting['setting']['type']](vcd)
        else:
            instance = VCDDumper.DumperFormaterList[VCDDumper.DumperTypeDefault](vcd)
        instance.init(setting['setting'] if 'setting' in setting else {})
        instance.timeline(setting['timescale'] if 'timescale' in setting else {})
        for sig in setting['signals']:
            instance.signal(sig)
        if 'dump' in setting:
            instance.dump(setting['dump'])
        return instance

    def __init__(self, vcd):
        assert isinstance(vcd, parser.VerilogVCD)
        self.vcd = vcd

    def init(self, args):
        "Initialization of Dumper"
        raise NotImplementedError

    def timeline(self, args):
        "Draw Timeline"
        raise NotImplementedError

    def signal(self, args):
        "Draw Each Signal line"
        raise NotImplementedError

    def dump(self, args):
        "Dump VCD to file with args"
        raise NotImplementedError

def register(name):
    'register a new Dumper'
    def _decorator(func):
        VCDDumper.DumperFormaterList[name] = func
        return func
    return _decorator
