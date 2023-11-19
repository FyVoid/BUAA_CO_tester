import re
import difflib

class Analyser:
    instructs = {}
    std = []
    cpu_output = []

    def __init__(self, std_name):
        self.load_std(std_name)

    def load_std(self, filename):
        self.std = []
        std_file = open(filename, "r")
        line_count = 0
        for line in std_file:
            if line_count >= 256:
                break
            m = re.match(r'@[\w]{8}: [\$*].+ <= [\w]{8}', line)
            if m:
                self.std.append(m.group(0))
                line_count += 1
        std_file.close()

    def analyse(self, filename, output_filename, save_log = True, show_first = False):
        output_file = open(output_filename, 'w')
        self.load_cpu_output(filename)
        diff = difflib.ndiff(self.std, self.cpu_output)
        flag = False
        for diffline in list(diff):
            if diffline.startswith('-') or diffline.startswith('+') or diffline.startswith('?'):
                flag = True
            output_file.write(diffline + '\n')

        if flag:
            output_file.write('Mismatch!\n')
        else:
            output_file.write('All Correct Nya!\n')
        
        output_file.close()

    def load_cpu_output(self, filename):
        cpu_output_file = open(filename, 'r')
        line_count = 0
        for line in cpu_output_file:
            if line_count >= 256:
                break
            m = re.match(r'@[\w]{8}: [\$*].+ <= [\w]{8}', line)
            if m:
                self.cpu_output.append(m.group(0))
                line_count += 1

class BatchAnalyser:
    batch_log = []
    log_filename = ""
    output_filename = ""

    def __init__(self, log_filename = "log.txt", output_filename='batch_log.txt'):
        self.batch_log = []
        self.log_filename = log_filename
        self.output_filename = output_filename

    def analyse(self, batch_dirname, dirname, batch_count):
        for i in range(batch_count):
            log = open(batch_dirname + '/' + dirname + '-{}/'.format(i) + self.log_filename, 'r')
            flag = True
            for line in log:
                if line.find('All Correct Nya!') >= 0:
                    flag = True
                    break
                if line.find("Mismatch!") >= 0:
                    flag = False
                    break
            log.close()
            self.batch_log.append(flag)

        output_file = open(self.output_filename, 'w')
        for i, flag in enumerate(self.batch_log):
            output_file.write("result of batch {}: ".format(i))
            if (flag):
                output_file.write("AC Nya!\n")
            else:
                output_file.write('failed!\n')
        output_file.close()
