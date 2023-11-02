from pytester import analyser

analyser = analyser.Analyser('std_output.txt')
analyser.analyse('cpu_output.txt', 'log.txt')