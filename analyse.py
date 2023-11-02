from pytester import analyser

analyser = analyser.Analyser('tester_log.txt')
analyser.analyse('cpu_output.txt', 'log.txt')