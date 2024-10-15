import subprocess

import os
import shutil

import warnings

import numpy as np

class Cacher():
    _n = 0
    def __init__(self):
        self.n = Cacher._n 
        self.n_files = 0
        Cacher._n += 1
        self.path = os.path.join(os.curdir, 'cache\\{}'.format(self.n))
        self.working = False
        if os.path.exists(self.path):
            shutil.rmtree(self.path)
        try:
            os.mkdir(self.path)
        except FileNotFoundError:
            os.mkdir(os.path.join(os.curdir, 'cache'))
            os.mkdir(self.path)

    def prepare(self):
        if self.working:
            raise RuntimeError('Another process is working on this cache')
        self.working = True
        self.stdin = os.path.join(self.path, 'input.txt'.format(self.n_files))
        self.stdout = os.path.join(self.path, 'output.txt'.format(self.n_files))
        self.stderr = os.path.join(self.path, 'errors.txt'.format(self.n_files))
        self.codefile = os.path.join(self.path, 'codefile.py')
    
    def writecode(self, code):
        with open(self.codefile, 'w', encoding='utf-8') as f:
            f.write(code)
    
    def writeinput(self, input):
        with open(self.stdin, 'w', encoding='utf-8') as f:
            f.write(input)
    
    def readoutput(self):
        with open(self.stdout, 'r', encoding='utf-8') as f:
            return f.read()

    def get_stdin(self):
        return open(self.stdin, 'r', encoding='utf-8')
    
    def get_stderr(self):
        return open(self.stderr, 'w', encoding='utf-8')

    def get_stdout(self):
        try:
            return open(self.stdout, 'a', encoding='utf-8')
        except FileNotFoundError:
            open(self.stdout, 'w')
            return open(self.stdout, 'a', encoding='utf-8')
    
    def readerrors(self):
        with open(self.stderr, 'r', encoding='utf-8') as f:
            return f.read()
    
    def clearoutput(self):
        open(self.stdout, 'w').close()
    
    def end(self):
        self.working = False
        os.remove(self.codefile)
        os.remove(self.stdin)
        os.remove(self.stdout)
        os.remove(self.stderr)

class Tester():
    def __init__(self, task):
        self.task = task
        self.cacher = Cacher()
    
    def evaluate(self, code, author_solution=False):
        if self.task.add:
            warnings.warn('Unable to run test: missing additional files')
            return []
        else:
            self.cacher.prepare()
            if not author_solution:
                code = '{}\n{}\n{}'.format(self.task.pre, code, self.task.post)
            self.cacher.writecode(code)
            results = [0]*len(self.task)
            for i, test in enumerate(self.task):
                self.cacher.writeinput(test.input+'\n')
                subprocess.Popen('python {}'.format(self.cacher.codefile),
                                 stdin=self.cacher.get_stdin(),
                                 stdout=self.cacher.get_stdout(),
                                 stderr=self.cacher.get_stderr()).wait()
                output = self.cacher.readoutput()
                errors = self.cacher.readerrors()
                self.cacher.clearoutput()
                results[i] = [((output == test.output or output == test.output + '\n') and not errors), output, errors]
            #self.cacher.end()
            return results

