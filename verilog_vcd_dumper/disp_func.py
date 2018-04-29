'disp func'

# TODO: z and x status not included

DISP_LIST = {
    'hex': lambda value: ('{:0>%dX}'%(len('   ' + value) // 4)).format(int(value, 2)),
    'bin': lambda x: x,
    'dec': lambda x: str(int(x, 2))
}
