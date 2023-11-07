import re

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
        cpu_out_count = 0
        tag = []
        flag = False
        for std_out in self.std:
            # you should use a better comparision method
            
            if len(self.cpu_output) <= cpu_out_count:
                output_file.write('-{}\n'.format(std_out))
                flag = True
            else:
                cpu_out = self.cpu_output[cpu_out_count]
                if std_out != cpu_out:
                    output_file.write('X{}: std\n'.format(std_out))
                    output_file.write('X{}: yours\n '.format(cpu_out))
                    for i, ch in enumerate(cpu_out):
                        if len(std_out) < i + 1 or ch != std_out[i]:
                            output_file.write('^')
                        else:
                            output_file.write(' ')
                    flag = True
                    output_file.write('\n')
                else:
                    output_file.write(' {}\n'.format(std_out))
            cpu_out_count += 1

        if len(self.cpu_output) > cpu_out_count:
            flag = True
            while cpu_out_count < len(self.cpu_output):
                output_file.write('+{}\n'.format(self.cpu_output[cpu_out_count]))
                cpu_out_count += 1

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
