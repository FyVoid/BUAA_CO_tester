import re

class Analyser:
    instructs = {}
    std = {}

    def __init__(self, std_name):
        self.load_std(std_name)

    def load_std(self, filename):
        self.std = []
        std_file = open(filename, "r")
        line_count = 0
        for line in std_file:
            if line_count >= 1000:
                break
            m = re.match(r'@([\w]{8}): ([\$*].+) <= ([\w]{8})', line)
            if m:
                addr = m.group(1)
                self.std.append((addr, m.group(2), m.group(3)))
                line_count += 1
        std_file.close()

    def analyse(self, filename, output_filename, save_log = True):
        cpu_output_file = open(filename, 'r')
        output_file = open(output_filename, 'w')
        line_count = 0
        mismatch = []
        for line in cpu_output_file:
            if line_count >= 1000:
                break
            if line.startswith('@'):
                addr = re.search(r'@([\w]{8}):', line).group(1)
                cpu_out = line[:-1]
                std_out = '@{}: {} <= {}'.format(addr, self.std[line_count][1], self.std[line_count][2])
                if cpu_out != std_out:
                    mismatch.append((line_count + 1, addr, cpu_out, std_out))
                if save_log:
                    output_file.write('{}{}<=>    {}\n'.format(cpu_out, (34 - len(cpu_out)) * ' ', std_out))
                line_count += 1

        output_file.write('END\n')
        if len(mismatch) <= 0:
            output_file.write('All Correct Nya!\n')
        else:
            output_file.write('Mismatch!\n')
            for mis in mismatch:
                self._log_err(output_file, mis)
        
        output_file.close()


    def _log_err(self, file, mis):
        file.write('error occurred at line {}, address {}, std out is {}, your output is {}\n'.format(mis[0], mis[1], mis[2], mis[3]))

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
            err_log = []
            flag = False
            for line in log:
                if flag:
                    if line.find('All Correct Nya!') >= 0:
                        err_log = []
                        break
                    else:
                        err_log.append(line)
                if line.startswith("END"):
                    flag = True
            self.batch_log.append(err_log)
            log.close()

        output_file = open(self.output_filename, 'w')
        for i, err_log in enumerate(self.batch_log):
            output_file.write("result of batch {}: ".format(i))
            if (len(err_log) > 0):
                output_file.write('failed!\n')
                for err in err_log:
                    output_file.write(err + '\n')
            else:
                output_file.write("AC Nya!\n")
        output_file.close()
