import re

class Analyser:
    instructs = {}

    def __init__(self, filename):
        self.load_log(filename)

    def load_log(self, filename):
        self.instructs = {}
        log_file = open(filename, "r")
        for line in log_file:
            m = re.match(r'(.+) # (.+)', line)
            if m:
                addr = m.group(2)
                self.instructs[addr] = m.group(1)

    def analyse(self, filename, output_filename):
        cpu_output_file = open(filename, 'r')
        output_file = open(output_filename, 'w')
        for line in cpu_output_file:
            if line.startswith('@'):
                addr = re.search(r'@([\w]{8}):', line).group(1)
                output_file.write('{}{}<=>     {}'.format(self.instructs[addr], ' ' * (25 - len(self.instructs[addr])), line))
    