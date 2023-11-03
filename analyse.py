from pytester import analyser as an
import sys
import os
import re

def main():
    dirname = ''
    save_log = True
    show_first = False
    if len(sys.argv) > 1:
        dirname = sys.argv[1]
        if not dirname.endswith('/'):
            dirname += '/'
    for arg in sys.argv:
        if arg.startswith("sl"):
            if re.match("sl:(.+)", arg).group(1) == 'false':
                save_log = False
        elif arg.startswith('sf'):
            if re.match('sf:(.+)', arg).group(1) == 'true':
                show_first = True
    if not os.path.exists(dirname) and dirname != '':
        os.mkdir(dirname)
    analyser = an.Analyser(dirname + 'std_output.txt')
    analyser.analyse(dirname + 'cpu_output.txt', dirname + 'log.txt', save_log = save_log, show_first = show_first)

if __name__ == "__main__":
    main()