import re
import random as rd

class Instruct:
    name = ""
    vars = []
    has_output = False

    types = {
        '$reg': {'t': 9, 's': 7, 'a': 3, 'v': 1},
        '$t': {'t': 9},
        '$s': {'s': 7},
        '$a': {'a': 3},
        '$v': {'v': 1},
        '$im': {'im': 0},
        '$lb': {'lb': 0},
        '$rega': {'rega': 0}
    }

    def __init__(self, name: str, vars: [str], has_output: bool = False):
        self.name = name
        self.vars = vars
        self.has_output = has_output

    def __init__(self, reg: str, has_output: bool = False):
        name_pattern = r'^[a-z]+'
        var_pattern = r'(\$[^,]+)'
        self.vars = []
        self.name = re.search(name_pattern, reg).group(0)
        for sep_var in reg.split(' '):
            var = re.search(var_pattern, sep_var)
            if var:
                self.vars.append(var.group(0))
        self.has_output = has_output

    def gen_instruct(self):
        ret = ''
        ret += self.name
        for var in self.vars:
            variable = self._rand_var(var)
            if variable:
                ret += ', ' + variable
            else:
                return None
        return ret
        
    def _rand_var(self, var: str):
        start = rd.choice(list(self.types[var].keys()))
        if start == 'im':
            return hex(rd.randint(0, 0xffff))
        elif start == 'lb':
            return "$label"
        elif start == 'rega':
            addr = int(get_legal_addr(), 16)
            offset = ((-1) ** rd.randint(1, 2)) * rd.randint(0, addr // 4) * 4
            base = addr - offset
            while base > 1024 * 4:
                offset = ((-1) ** rd.randint(1, 2)) * rd.randint(0, addr // 4) * 4
                base = addr - offset
            return '{}({})'.format(offset, base)
            # return '{}({})'.format(get_legal_addr(), '$t0')
        else:
            return '${}{}'.format(start, rd.randint(0, self.types[var][start]))

def get_legal_addr():
    return hex(int(rd.randint(0, 248)) * 4)
