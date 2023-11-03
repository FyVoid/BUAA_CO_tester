from pytester import analyser as an
import sys

def main():
    batch_dirname = sys.argv[1]
    dirname = sys.argv[2]
    batch_count = int(sys.argv[3])
    banalyser = an.BatchAnalyser()
    banalyser.analyse(batch_dirname, dirname, batch_count)

if __name__ == '__main__':
    main()