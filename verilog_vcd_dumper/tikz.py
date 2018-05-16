'tikz dumper'
import io
from . import dumper
from . import utils

# pylint: disable=W0201, C0103

@dumper.register('tikz')
class TikzDumper(dumper.VCDDumper):
    "Dump VCD to Tikz TeX file"

    def init(self, args):
        # print([self.vcd.data[i]['nets'] for i in self.vcd.data.keys()])
        self.top = 0
        self.fp = io.StringIO()
        self.indent = 2 if not 'indent' in args else args['indent']
        self.lineheight = 0.8 if not 'lineheight' in args else args['lineheight']
        self.gapwidth = 0.08 if not 'gapwidth' in args else args['gapwidth']
        self.scale = 0.2 if not 'scale' in args else args['scale']
        self.write("\\begin{tikzpicture}", indent=0)

    def write(self, *value, indent=1, end="\n", sep=' '):
        'print to file with indent'
        print(' '*self.indent*indent, end='', file=self.fp)
        print(*value, sep=sep, end=end, file=self.fp)

    def timeline(self, args):
        self.time_start = utils.divide_with_unit(args['start'], self.vcd.timescale)
        self.time_end = utils.divide_with_unit(args['end'], self.vcd.timescale)

    def signal(self, args):
        args = utils.intelligent_arg(args)
        sym, osy, index = utils.find_symbol(self.vcd, args['id'])
        if not 'label' in args:
            label = utils.tex_escape(osy['name'])
        else:
            if callable(args['label']):
                label = args['label'](osy)
            else:
                label = args['label']
        size = int(osy['size'])
        _tv = self.vcd.data[sym]['tv']
        if 'disp' in args:
            if callable(args['disp']):
                disp = args['disp']
            else:
                disp = utils.DISP_LIST[args['disp']]
        else:
            disp = utils.DISP_LIST['hex']
        print(size, sym, label, index)
        self.write("% {}.{}".format(osy['hier'], osy['name']))
        self.write("\\draw node[left] at ({}, {}) {{{}}};".format(-0.5, self.top, label))
        if size == 1:
            # binary wave
            data = self.vcd.data[sym]['tv']
            pointer = 0
            while data[pointer][0] < self.time_start:
                pointer += 1
            while data[pointer][0] < self.time_end:
                _s = self.scale * data[pointer][0]
                _e = self.scale * data[pointer + 1][0]
                _hh = self.lineheight / 2 * 0.8
                _t = self.top
                _sd = int(data[pointer][1]) * 2 * _hh + _t - _hh
                _ed = int(data[pointer + 1][1]) * 2 * _hh + _t - _hh
                self.write("\\draw ({}, {}) -- ({}, {}) -- ({}, {});".format(
                    _s, _sd, _e, _sd, _e, _ed))
                pointer += 1
        else:
            # multi wave
            data = self.vcd.data[sym]['tv']
            pointer = 0
            while data[pointer][0] < self.time_start:
                pointer += 1
            while data[pointer][0] < self.time_end:
                print(data[pointer])
                _s = self.scale * data[pointer][0]
                _e = self.scale * data[pointer + 1][0]
                _g = self.gapwidth / 2
                _hh = self.lineheight / 2 * 0.9
                _t = self.top
                self.write("\\draw")
                self.write("  ({}, {}) -- ({}, {}) -- ({}, {}) --".format(
                    _s, _t, _s + _g, _t + _hh, _e - _g, _t + _hh))
                self.write("  ({}, {}) -- ({}, {}) -- ({}, {}) --".format(
                    _e, _t, _e - _g, _t - _hh, _s + _g, _t - _hh))
                self.write("  ({}, {});".format(_s, _t))
                self.write("\\draw node[right] at ({}, {}) {{\\texttt{{{}}}}};".format(
                    _s, _t, disp(data[pointer][1])))
                pointer += 1
        self.top -= self.lineheight

    def final(self, args):
        self.write("\\end{tikzpicture}", indent=0)

    def dump(self, args=None):
        return self.fp.getvalue()

dumper.VCDDumper.DumperFormaterList['latex'] = TikzDumper
dumper.VCDDumper.DumperFormaterList['tex'] = TikzDumper
