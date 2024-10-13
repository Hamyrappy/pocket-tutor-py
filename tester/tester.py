import subprocess
import pandas as pd
import os

class Cacher():
    _n = 0
    def __init__(self)
        self.n = Cacher._n 
        self.n_files = 0
        Cacher._n += 1
        self.path = os.path.join(os.curdir, 'cache/{}'.format(self.n))
        if os.path.exist(self.path):
            os.rmdir(self.path)
        os.mkdir(self.path)
    def newfile(self, *args, **kwargs):
        path = os.path.join(self.path, self.n_files)
        self.n_files += 1
        return path, open(os.path.join(self.path), *args, **kwargs)

class Tester():
    def __init__(self, tasks_path, tests_path):
        self.tasks = pd.read_excel(tasks_path)
        self.tests = pd.read_excel(tests_path)
        self.cacher = Cacher()
    
    def evaluate(self, code):
        path, codefile = self.cacher.newfile('w')
        codefile.write(code)
        subprocess.Popen('python {}'.format(path))
    