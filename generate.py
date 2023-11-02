from pytester import tester

tester = tester.Tester('tester_config.txt')
tester.gen_assembly('assemble.asm', 114)