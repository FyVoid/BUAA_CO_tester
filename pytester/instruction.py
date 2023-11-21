import re
import random as rd

class Instruct:
    name = ""
    vars = []
    _max_legal_addr = 248
    jump = False
    used_reg = 0.0

    types = {
        '$reg': {'t': 9, 's': 7, 'a': 3, 'v': 1},
        '$t': {'t': 9},
        '$s': {'s': 7},
        '$a': {'a': 3},
        '$v': {'v': 1},
        '$im': {'im': 0},
        '$lb': {'lb': 0},
        '$rega': {'rega': 0},
        '$regaddr': {'regaddr': 0}
    }

    def __init__(self, name: str, vars: [str], jump=False, used_reg=0.0):
        self.name = name
        self.vars = vars
        self.jump = jump
        self.used_reg = used_reg

    def __init__(self, reg: str, jump=False, used_reg=0.0):
        name_pattern = r'^[a-z]+'
        var_pattern = r'(\$[^,]+)'
        self.vars = []
        self.name = re.search(name_pattern, reg).group(0)
        for sep_var in reg.split(' '):
            var = re.search(var_pattern, sep_var)
            if var:
                self.vars.append(var.group(0))
        self.jump = jump
        self.used_reg = used_reg

    def gen_instruct(self, used_regs=[]):
        ret = ''
        ret += self.name
        for var in self.vars:
            variable = self._rand_var(var, used_regs)
            if variable:
                ret += ', ' + variable
            else:
                return None
        return ret

    def _rand_var(self, var: str, used_regs):
        used = self.used_reg > rd.random()

        start = rd.choice(list(self.types[var].keys()))

        if start == 'im':
            return hex(rd.randint(0, 0xffff))

        elif start == 'lb':
            return "$label"

        elif start == 'rega':
            addr = int(self.get_legal_addr(), 16)
            offset = rd.randint(0, addr // 4) * 4
            base = addr - offset
            while base > self._max_legal_addr * 4:
                offset = rd.randint(0, addr // 4) * 4
                base = addr - offset
            return '{}({})'.format(offset, base)
        
        elif start == 'regaddr':
            addr = int(self.get_legal_addr(), 16)
            offset = rd.randint(0, addr)
            base = addr - offset
            while base > self._max_legal_addr * 4:
                offset = rd.randint(0, addr)
                base = addr - offset
            return '{}({})'.format(offset, base)

        else:
            if used and len(used_regs) > 0:
                return rd.choice(used_regs)
            else:
                ret = '${}{}'.format(start, rd.randint(0, self.types[var][start]))
                if ret not in used_regs:
                    used_regs.append(ret)
                return ret

    def get_legal_addr(self):
        return hex(int(rd.randint(0, self._max_legal_addr)) * 4)
