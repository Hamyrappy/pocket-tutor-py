'''Datamanager object for solutions, tasks and tests.'''

import pandas as pd
import os.path as osp
from functools import lru_cache as cache
import numpy as np
import re
import warnings

def replace_nan(x, tp=str):
    """
    Replace NaN values in the input with a specified value.

    Parameters
    ----------
    x : any
        The input value to check for NaN.
    tp : any, optional
        Type of valueto replace NaN with (default is str).

    Returns
    -------
    any
        The original input if it's not NaN, otherwise the specified replacement value.
    """
    if isinstance(x, str):
        return tp(x)
    elif np.isnan(x):
        return tp()
    else:
        return tp(x)

class Test():
    def __init__(self, info):
        """
        Initialize the Test object.

        Parameters
        ----------
        info : pandas.DataFrame
            A DataFrame containing the test information.
        """
        self.number = info['number']
        self.input = replace_nan(info['input'])
        self.output = replace_nan((info['output']))
        self.type = info['type']
        self.id = info['id']
        self.task_id = info['task_id']

class Task():
    def __init__(self, tests, solutions, info):
        """
        Initialize the Task object.

        Parameters
        ----------
        tests : pandas.DataFrame
            The DataFrame with all the tests for the task.
        solutions : pandas.DataFrame
            The DataFrame with all the solutions for the task.
        info : pandas.DataFrame
            The DataFrame with task info (id, level, description, author_solution, pre, post, add).
        """
        self.tests = [Test(tests[tests['number'] == index].to_dict('records')[0]) for index in range(len(tests))]
        solutions = solutions.to_dict('records')
        self.solutions = [Solution(solution) for solution in solutions]
        self.id = info['id']
        self.level = info['level']
        self.desription = info['description']
        self.author_solution = info['author_solution']
        self.pre = replace_nan(info['pre'])
        self.post = replace_nan(info['post'])
        self.add = replace_nan(info['add'])

    def __len__(self):
        return len(self.tests)

class Solution():
    def __init__(self, info):
        self.solution = info['student_solution']
        self.id = info['id']
        self.task_id = info['task_id']
        self.author_comment = info['author_comment']
    
    def test(self, tester):
        test_results = tester.test(self.solution)
        if not test_results:
            return {'correct': None, 'report': 'Тесты не удалось запустить', 'syntax_error':False,  'error_on_open': False, 'error_on_closed': False}
        error_on_open = False
        error_on_closed = False
        verdicts = {}
        syntax_error = False
        for result, test in zip(test_results, tester.task.tests):
            if not result[0]:
                if test.type == 'open':
                    error_on_open = True
                else:
                    error_on_closed = True
                
                if result[2]:
                    if not 'RuntimeError'in verdicts:
                        verdicts['RuntimeError'] = {'input':test.input, 'errors':result[2]}
                    if re.search('SyntaxError', result[2]):
                        syntax_error = True
                        report = '''В коде решения присутствует синтаксическая ошибка. Лог: {}'''.format(result[2])
                        error_on_open = True
                        error_on_closed = True
                        break
                else:
                    if not 'WrongAnswer' in verdicts:
                        verdicts['WrongAnswer'] = {'input':test.input, 'answer':test.output, 'output':result[1]}
                
        if not error_on_open and not error_on_closed:           
            return {'correct': True, 'report': 'Решение прошло все тесты', 'syntax_error':False,  'error_on_open': False, 'error_on_closed': False}
        report = ''
        if 'WrongAnswer' in verdicts:
            WA_report = '''На одном из тестов решение вернуло неверный ответ.
Ввод теста:
{input}
Ожидаемый ответ:
{answer}
Ответ решения:
{output}
'''.format(**verdicts['WrongAnswer'])
            report += WA_report
        if 'RuntimeError' in verdicts:
            error_report = '''На одном из тестов решение выполнилось с ошибкой.
Ввод теста:
{input}
Лог:
{errors}
'''.format(**verdicts['RuntimeError'])
            report += error_report
        return {'correct': False, 'report': report, 'syntax_error':syntax_error,  'error_on_open': error_on_open, 'error_on_closed': error_on_closed}
    
    
class DataManager:
    '''Class to hold data for tasks, tests and solutions.
    Usage:
    >>> dm = DataManager('path/to/data') # в директории должны быть файлы tasks.xlsx, tests.xlsx и solutions.xlsx
    >>> task = dm[0] #Таск с номером 0
    >>> test = task.tests[0] #Тест для таска 0 с номером 0
    >>> solutions = task.solutions #Список с решениями таска 0
    '''
    def __init__(self, path):
        """
        Initialize the DataManager object.

        Parameters
        ----------
        path : str
            The path to the folder with tasks.xlsx, tests.xlsx and solutions.xlsx files.
        """
        self.path = path
        self.tasks = pd.read_excel(osp.join(path, 'tasks.xlsx'))
        self.tests = pd.read_excel(osp.join(path, 'tests.xlsx'))
        self.solutions = pd.read_excel(osp.join(path, 'solutions.xlsx'))

    def get_task(self, index):
        """
        Get a task by its index.

        Parameters
        ----------
        index : int
            The index of the task in the DataManager.

        Returns
        -------
        task : Task
            Task object with the given index.
        """
        task_id = self.tasks['id'].to_numpy(dtype=int)[index]
        return self.get_task_by_id(task_id)
    
    def get_task_by_id(self, task_id):
        """
        Get a task by its ID.

        Parameters
        ----------
        task_id : int
            The ID of the task to retrieve.

        Returns
        -------
        Task
            Task object with the given ID.
        """
        tests = self.tests[self.tests.task_id == task_id]
        solutions = self.solutions[self.solutions.task_id == task_id]
        return Task(tests, solutions, self.tasks[self.tasks['id'] == task_id].to_dict('records')[0])
    
    def __len__(self):
        return len(self.tasks)

    def __getitem__(self, index):
        return self.get_task(index)
