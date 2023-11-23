from pytester import tester as ts
from pytester import analyser
import sys
import os

gen_label_prob = 0.2
former_addr_prob = 0.5
total_instruct = 40
total_block = 5

def main():
    dirname = ''
    if len(sys.argv) > 1:
        dirname = sys.argv[1]
        if not dirname.endswith('/'):
            dirname += '/'
    if not os.path.exists(dirname) and dirname != '':
        os.mkdir(dirname)
    tester = ts.Tester('tester_config.txt')
    tester.gen_label_prob = gen_label_prob
    tester.former_addr_prob = former_addr_prob
    tester.gen_assembly(dirname + 'assemble.asm', total_block, total_instruct)

if __name__ == '__main__':
    main()