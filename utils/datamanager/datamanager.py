'''Datamanager object for solutions, tasks and tests.'''

import pandas as pd
import os.path as osp
from functools import lru_cache as cache
import numpy as np

def replace_nan(x, value=''):
    """
    Replace NaN values in the input with a specified value.

    Parameters
    ----------
    x : any
        The input value to check for NaN.
    value : any, optional
        The value to replace NaN with (default is '').

    Returns
    -------
    any
        The original input if it's not NaN, otherwise the specified replacement value.
    """
    if isinstance(x, str):
        return x
    elif np.isnan(x):
        return value
    else:
        return x

class Test():
    def __init__(self, info):
        """
        Initialize the Test object.

        Parameters
        ----------
        info : pandas.DataFrame
            A DataFrame containing the test information.
        """
        self.number = replace_nan(info['number'].to_numpy()[0])
        self.input = str(replace_nan(info['input'].to_numpy()[0]))
        self.output = str(replace_nan(info['output'].to_numpy()[0]))
        self.type = replace_nan(info['type'].to_numpy()[0])
        self.id = replace_nan(info['id'].to_numpy()[0])
        self.task_id = replace_nan(info['task_id'].to_numpy()[0])

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
        self.tests = tests
        self.solutions = solutions
        self.id = replace_nan(info['id'].to_numpy()[0])
        self.level = replace_nan(info['level'].to_numpy()[0])
        self.desription = replace_nan(info['description'].to_numpy()[0])
        self.author_solution = replace_nan(info['author_solution'].to_numpy()[0])
        self.pre = replace_nan(info['pre'].to_numpy()[0])
        self.post = replace_nan(info['post'].to_numpy()[0])
        self.add = replace_nan(info['add'].to_numpy()[0])
    
    @cache
    def __getitem__(self, index):
        return Test(self.tests[self.tests['number'] == index])

    def __len__(self):
        return len(self.tests)
        
class DataManager:
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
        task_id = self.tasks['id'].to_numpy()[index]
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
        return Task(tests, solutions, self.tasks[self.tasks['id'] == task_id])
    
    def __len__(self):
        return len(self.tasks)

    def __getitem__(self, index):
        return self.get_task(index)
