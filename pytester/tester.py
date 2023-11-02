import random as rd
from . import instruction
import re

class Tester:
    labels = []
    instructs = {}
    instruct_prob = {}
    buffer = []
    gen_label_prob = 0.2
    former_addr_prob = 0.5

    def __init__(self, config_file: str):
        self.labels = []
        self.load_config(config_file)

    def load_config(self, config_file: str):
        self.instructs = {}
        self.instruct_prob = {}
        self.buffer = []
        config = open(config_file, "r")
        for line in config:
            line_split = line.split('|')
            output = False
            label = False
            prob = 0
            if len(line_split) > 1:
                if line_split[1].find('output') > 0:
                    output = True
                if re.search(r'prob:\s*(.+)f', line_split[1]):
                    prob = float(re.search(r'prob:\s*(.+)f', line_split[1]).group(1))
            ist = instruction.Instruct(line_split[0], has_output=output)
            self.instructs[ist.name] = ist
            self.instruct_prob[ist.name] = prob
        config.close()
        total_prob = 1
        total_unfilled = 0
        for name in self.instruct_prob.keys():
            if self.instruct_prob[name] == 0:
                total_unfilled += 1
            total_prob -= self.instruct_prob[name]
        for name in self.instruct_prob.keys():
            if self.instruct_prob[name] == 0:
                self.instruct_prob[name] = total_prob / total_unfilled
        print(self.instruct_prob)

    def _rand_label(self):
        label = 'label' + str(len(self.labels))
        if len(self.labels) > 0:
            if rd.random() <= self.gen_label_prob:
                self.labels.append(label)
            else:
                label = rd.choice(self.labels)
        else:
            self.labels.append(label)
        return label
    
    def gen_assembly(self, filename: str, total_instruct: int):
        instruct_extractor = []
        former_addr = []
        self.buffer = []
        self.labels = []
        ra_saved = False
        for name in self.instruct_prob.keys():
            instruct_extractor += [name] * (int)(self.instruct_prob[name] * 100)
        rd.shuffle(instruct_extractor)
        target_file = open(filename, 'w')
        i = 0
        while i < total_instruct:
            name = rd.choice(instruct_extractor)
            ist = self.instructs[name]
            if name == 'jalr':
                ra_saved = True
            if name == 'jr':
                if not ra_saved:
                    i -= 1
                    continue
                self.buffer.append(('jr $ra', True))
            else:
                instruct_str = ist.gen_instruct()
                if instruct_str.find('$label') > 0:
                    instruct_str = instruct_str.replace('$label', self._rand_label())
                if re.search(r'-*\d+\(-*\d+\)', instruct_str):
                    pt = re.search(r'(-*\d+)\((-*\d+)\)', instruct_str)
                    offset = pt.group(1)
                    base = pt.group(2)
                    if len(former_addr) > 0 and rd.random() > self.former_addr_prob:
                        self.buffer.append(('ori $t0, $zero, {}'.format(rd.choice(former_addr)), True))
                        i += 1
                        instruct_str = instruct_str.replace(base, '$t0').replace(offset, '0')
                    else:
                        self.buffer.append(('ori $t0, $zero, {}'.format(base), True))
                        former_addr.append(int(offset) + int(base))
                        i += 1
                        instruct_str = instruct_str.replace(base, '$t0')
                self.buffer.append((instruct_str, ist.has_output))
            i += 1

        for label in self.labels:
            self.buffer.insert(rd.randint(0, len(self.buffer)), (label + ':', False))
        target_file.write(".text\n")
        for ist_str in self.buffer:
            target_file.write(ist_str[0] + '\n')
