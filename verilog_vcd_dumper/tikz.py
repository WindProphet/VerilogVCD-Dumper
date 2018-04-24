'tikz dumper'
from . import dumper
from . import utils

# pylint: disable=W0201

@dumper.register('tikz')
class TikzDumper(dumper.VCDDumper):
    "Dump VCD to Tikz TeX file"

    def init(self, args):
        # print([self.vcd.data[i]['nets'] for i in self.vcd.data.keys()])
        self.top = 0

    def timeline(self, args):
        self.time_start = utils.divide_with_unit(args['start'], self.vcd.timescale)
        self.time_end = utils.divide_with_unit(args['end'], self.vcd.timescale)

    def signal(self, args):
        args = utils.intelligent_arg(args)
        sym, osy, index = utils.find_symbol(self.vcd, args['id'])
        if not 'label' in args:
            label = osy['name']
        else:
            if callable(args['label']):
                label = args['label'](osy)
            else:
                label = args['label']
        size = int(osy['size'])
        _tv = self.vcd.data[sym]['tv']
        print(size, sym, label, index)

    def dump(self, args):
        pass

dumper.VCDDumper.DumperFormaterList['latex'] = TikzDumper
dumper.VCDDumper.DumperFormaterList['tex'] = TikzDumper
