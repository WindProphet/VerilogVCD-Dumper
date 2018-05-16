'utils for dumper'
import re

from . import disp_func
DISP_LIST = disp_func.DISP_LIST

IDENTITY_REGEXP = re.compile(r"^(.*?)(?:\[(.*?)\])?$")
TOPMODULE = 'TOP'

def find_symbol(self, sym):
    'find symbol from VerilogVCD'
    splitsym = sym.rsplit('.', 1)
    if len(splitsym) == 1:
        splitsym.insert(0, None)
    hier, name = splitsym
    if not hier is None:
        if hier == '':
            hier = TOPMODULE
        elif hier[0] == '.':
            hier = TOPMODULE + '.' + hier[1:]
    for i in self.data.keys():
        for osy in self.data[i]['nets']:
            match = IDENTITY_REGEXP.match(osy['name'])
            barename = match.group(1)
            try:
                index = match.group(2)
            except IndexError:
                index = None
            if hier is None:
                if barename == name:
                    return (i, osy, index)
            else:
                if barename == name and (
                        osy['hier'] == hier or
                        osy['hier'] == (TOPMODULE + '.' + hier)):
                    return (i, osy, index)
    return (None, None, None)

def intelligent_arg(arg):
    'intelligent detect signal arg'
    if isinstance(arg, str):
        return {'id': arg}
    elif isinstance(arg, tuple):
        # TODO: tuple for signals id
        return {'id': arg[0]}
    return arg

def divide_with_unit(time, base):
    'divide time of string with unit'
    regex = re.compile(r"^([\d\.]*)([a-z]?s)?$")
    time_m = regex.match(time)
    base_m = regex.match(base)
    mults = {
        'fs' : -15,
        'ps' : -12,
        'ns' : -9,
        'us' : -6,
        'ms' : -3,
        's' : 0,
    }
    if not (time_m and base_m):
        raise ValueError("invaild time format")
    if time_m.lastindex == 1:
        return int(time)
    try:
        time_u = mults[time_m.group(2)]
        base_u = mults[base_m.group(2)]
    except KeyError:
        raise ValueError("invaild unit")
    import math
    # rel_t = float(time_m.group(1)) * math.pow(10, (time_u - base_u)) / float(base_m.group(1))
    rel_t = int(int(time_m.group(1)) * int(math.pow(10, (time_u - base_u))) / int(base_m.group(1)))
    return rel_t

def tex_escape(value: str):
    'tex escape special symbols'
    return value.replace('_', '\\_')
