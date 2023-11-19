import random as rd
from . import instruction
import re

class Tester:
    labels = []
    instructs = {}
    jump_instructs = {}
    instruct_prob = {}
    jump_instruct_prob = {}
    blocks = []
    former_addr = []
    used_regs = []
    gen_label_prob = 0.2
    former_addr_prob = 0.5

    def __init__(self, config_file: str):
        self.labels = []
        self.load_config(config_file)

    def load_config(self, config_file: str):
        self.instructs = {}
        self.instruct_prob = {}

        self.jump_instructs = {}
        self.jump_instruct_prob = {}

        self.buffer = []
        config = open(config_file, "r")

        for line in config:
            line_split = line.split('|')
            prob = 0
            jump = False
            used_reg = 0.0

            if len(line_split) > 1:
                if re.search('jump', line_split[1]):
                    jump = True

                if re.search('used_reg:\s*([^f]+)f?', line_split[1]):
                    used_reg = float(re.search(r'used_reg:\s*([^f]+)f?', line_split[1]).group(1))

                if re.search(r'prob:\s*([^f]+)f?', line_split[1]):
                    prob = float(re.search(r'prob:\s*([^f]+)f?', line_split[1]).group(1))

            ist = instruction.Instruct(line_split[0], jump=jump, used_reg=used_reg)

            if jump:
                self.jump_instructs[ist.name] = ist
                self.jump_instruct_prob[ist.name] = prob
            else:
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

        total_prob = 1
        total_unfilled = 0
        for name in self.jump_instruct_prob.keys():
            if self.jump_instruct_prob[name] == 0:
                total_unfilled += 1
            total_prob -= self.jump_instruct_prob[name]
        for name in self.jump_instruct_prob.keys():
            if self.jump_instruct_prob[name] == 0:
                self.jump_instruct_prob[name] = total_prob / total_unfilled

        print(self.instruct_prob)
        print(self.jump_instruct_prob)

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

    def gen_assembly_block(self, instruct_extractor, total_instruct=100):
        buffer = []
        i = 0
        while i < total_instruct:
            name = rd.choice(instruct_extractor)
            ist = self.instructs[name]

            instruct_str = ist.gen_instruct(self.used_regs)

            if re.search(r'-*\d+\(-*\d+\)', instruct_str):
                pt = re.search(r'(-*\d+)\((-*\d+)\)', instruct_str)
                offset = pt.group(1)
                base = pt.group(2)

                # old address
                if len(self.former_addr) > 0 and rd.random() > self.former_addr_prob:
                    self.buffer.append(('ori $t0, $zero, {}'.format(hex(int(rd.choice(self.former_addr)))), True))
                    i += 1
                    instruct_str = instruct_str.replace('(' + base + ')', '($t0)').replace(offset, '0')
                # new address
                else:
                    self.buffer.append(('ori $t0, $zero, {}'.format(hex(int(base))), True))
                    self.former_addr.append(int(offset) + int(base))
                    i += 1
                    instruct_str = instruct_str.replace('(' + base + ')', '($t0)')

            buffer.append(instruct_str)
            i += 1

        return buffer

    def gen_assembly(self, filename, total_blocks, block_instruct_count=100):
        instruct_extractor = []
        for name in self.instruct_prob.keys():
            instruct_extractor += [name] * (int)(self.instruct_prob[name] * 300)
        rd.shuffle(instruct_extractor)

        self.former_addr = []
        self.used_regs = []
        self.blocks = []
        labels = []

        for block_count in range(total_blocks):
            self.blocks.append(self.gen_assembly_block(instruct_extractor, block_instruct_count))
            labels.append('label{}'.format(block_count))

        rd.shuffle(labels)
        jump_instruct_extractor = []
        for name in self.jump_instruct_prob.keys():
            jump_instruct_extractor += [name] * (int)(self.jump_instruct_prob[name] * 300)
        rd.shuffle(jump_instruct_extractor)

        # insert jump
        if len(jump_instruct_extractor) > 0:
            for index, block in enumerate(self.blocks):
                name = rd.choice(jump_instruct_extractor)
                ist = self.jump_instructs[name]

                instruct_str = ist.gen_instruct()

                if name == 'jr':
                    block.insert(-1, 'jr $ra')
                else:
                    instruct_str = instruct_str.replace('$label', labels[index])
                    block.insert(-1, instruct_str)

                block.insert(0, labels[index] + ':')

        target_file = open(filename, 'w')
        target_file.write('.text\n')
        target_file.write('ori $ra, $zero, 0x3000\n\n')

        for block in self.blocks:
            for instruct in block:
                target_file.write('{}\n'.format(instruct))

            target_file.write('\n')

        target_file.close()

    # def gen_assembly(self, filename: str, total_instruct: int):
    #     instruct_extractor = []
    #     former_addr = []
    #     self.buffer = []
    #     self.labels = []
    #     ra_saved = False
    #     for name in self.instruct_prob.keys():
    #         instruct_extractor += [name] * (int)(self.instruct_prob[name] * 300)
    #     rd.shuffle(instruct_extractor)
    #     target_file = open(filename, 'w')
    #     i = 0
    #     while i < total_instruct:
    #         name = rd.choice(instruct_extractor)
    #         ist = self.instructs[name]
    #         if name == 'jal':
    #             ra_saved = True
    #         if name == 'jr':
    #             if not ra_saved:
    #                 i -= 1
    #                 continue
    #             self.buffer.append(('jr $ra', True))
    #         else:
    #             instruct_str = ist.gen_instruct()
    #             if instruct_str.find('$label') > 0:
    #                 instruct_str = instruct_str.replace('$label', self._rand_label())
    #             if re.search(r'-*\d+\(-*\d+\)', instruct_str):
    #                 pt = re.search(r'(-*\d+)\((-*\d+)\)', instruct_str)
    #                 offset = pt.group(1)
    #                 base = pt.group(2)
    #                 if len(former_addr) > 0 and rd.random() > self.former_addr_prob:
    #                     self.buffer.append(('ori $t0, $zero, {}'.format(hex(int(rd.choice(former_addr)))), True))
    #                     i += 1
    #                     instruct_str = instruct_str.replace('(' + base + ')', '($t0)').replace(offset, '0')
    #                 else:
    #                     self.buffer.append(('ori $t0, $zero, {}'.format(hex(int(base))), True))
    #                     former_addr.append(int(offset) + int(base))
    #                     i += 1
    #                     instruct_str = instruct_str.replace('(' + base + ')', '($t0)')
    #             self.buffer.append((instruct_str, ist.has_output))
    #         i += 1
    #
    #     for label in self.labels:
    #         self.buffer.insert(rd.randint(0, len(self.buffer)), (label + ':', False))
    #     target_file.write(".text\n")
    #     addr = int(0x3000)
    #     for ist_str in self.buffer:
    #         target_file.write(ist_str[0] + '\n')
    #         if not ist_str[0].startswith('label'):
    #             addr += 4