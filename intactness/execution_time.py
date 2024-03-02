from time import time
from math import floor

# track runtime of each pipeline

class ExecutionTime:
    def __init__(self, path):
        self.start_time = time()
        self.file = f"{path}/execution_time.txt"
        self.write('init')

    #overwrite file contents
    def write(self, content):
        with open(self.file, 'w') as f:
            f.write(content)

    def finish(self):
        self.write(f'{floor((time() - self.start_time)/60)} minutes')