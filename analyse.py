from pytester import analyser as an
import sys
import os

def main():
    dirname = ''
    save_log = True
    if len(sys.argv) > 1:
        dirname = sys.argv[1]
        if not dirname.endswith('/'):
            dirname += '/'
    for arg in sys.argv:
        if arg == 'false':
            save_log = False
    if not os.path.exists(dirname) and dirname != '':
        os.mkdir(dirname)
    analyser = an.Analyser(dirname + 'std_output.txt')
    analyser.analyse(dirname + 'cpu_output.txt', dirname + 'log.txt', save_log = save_log)

if __name__ == "__main__":
    main()