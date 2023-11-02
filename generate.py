from pytester import tester
from pytester import analyser

tester = tester.Tester('tester_config.txt')
tester.gen_assembly('assemble.asm', 114)