from pytester import tester
from pytester import analyser

gen_label_prob = 0.2
former_addr_prob = 0.5
total_instruct = 114

tester = tester.Tester('tester_config.txt')
tester.gen_label_prob = gen_label_prob
tester.former_addr_prob = former_addr_prob
tester.gen_assembly('assemble.asm', total_instruct=total_instruct)