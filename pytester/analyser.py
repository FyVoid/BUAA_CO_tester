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