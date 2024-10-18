import subprocess

import os
import shutil

import warnings

import pandas as pd

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
            f.write(input+'\n')
    
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
        for filepath in [self.codefile, self.stdin, self.stdout, self.stderr]:
            try:
                os.remove(filepath)
            except FileNotFoundError:
                pass

class Tester():
    '''Class for testing solutions against single task. Usage:
    >>> dm = DataManager('path/to/data') 
    >>> task = dm[0]
    >>> tester = Tester(task)
    >>> results = tester.test(code)
    >>> results[0] # результат решения на тесте 0 - список [пройдено или нет, вывод, ошибки]
    [True, 'output', 'errors']'''
    def __init__(self, task):
        """
        Create a new Tester instance.

        Parameters
        ----------
        task : Task
            The task to test.
        """
        
        self.task = task
        self.cacher = Cacher()
    
    def test(self, code):
        """
        Test a code solution against a task.

        Parameters
        ----------
        code : str
            The code to test.

        Returns
        -------
        results : list of list of (bool, str, str)
            A list of tuples. For each test, the first element is a boolean indicating whether the test was passed, the second element is the output of the code, and the third element is any error output.

        Notes
        -----
        If the task requires additional files, a warning will be raised and an empty list will be returned.
        Да, всё так. Какие-то задачи  требуют прочитать блаблабла.csv, которого у нас неть
        """
        if not pd.isna(self.task.add) and self.task.add:
            warnings.warn('Unable to run test: missing additional files')
            return []
        else:
            self.cacher.prepare()
            code = '{}\n{}\n{}'.format(self.task.pre, code, self.task.post)
            self.cacher.writecode(code)
            results = [0]*len(self.task)
            for i, test in enumerate(self.task.tests):
                self.cacher.writeinput(test.input+'\n')
                abspath = os.path.abspath(self.cacher.codefile)
                subprocess.Popen(["python", abspath],
                                 stdin=self.cacher.get_stdin(),
                                 stdout=self.cacher.get_stdout(),
                                 stderr=self.cacher.get_stderr()).wait()
                output = self.cacher.readoutput()
                errors = self.cacher.readerrors()
                self.cacher.clearoutput()
                results[i] = [((output == test.output or output == test.output + '\n') and not errors), output, errors]
            self.cacher.end()
            return results

