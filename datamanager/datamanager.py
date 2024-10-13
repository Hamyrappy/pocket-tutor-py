import pandas as pd
import os.path as osp
from functools import lru_cache as cache

class Test():
    def __init__(self, info):
        self.number = info['number'].to_numpy()[0]
        self.input = info['input'].to_numpy()[0]
        self.output = info['output'].to_numpy()[0]
        self.type = info['type'].to_numpy()[0]
        self.id = info['id'].to_numpy()[0]
        self.task_id = info['task_id'].to_numpy()[0]

class Task():
    def __init__(self, tests, solutions, info):
        self.tests = tests
        self.solutions = solutions
        self.id = info['id'].to_numpy()[0]
        self.level = info['level'].to_numpy()[0]
        self.desription = info['description'].to_numpy()[0]
        self.author_solution = info['author_solution'].to_numpy()[0]
    
    @cache
    def __getitem__(self, index):
        return Test(self.tests[self.tests['number'] == index])

    def __len__(self):
        return len(self.tests)
        
class DataManager:
    def __init__(self, path):
        self.path = path
        self.tasks = pd.read_excel(osp.join(path, 'tasks.xlsx'))
        self.tests = pd.read_excel(osp.join(path, 'tests.xlsx'))
        self.solutions = pd.read_excel(osp.join(path, 'solutions.xlsx'))

    def get_task(self, index):
        task_id = self.tasks['id'].to_numpy()[index]
        return self.get_task_by_id(task_id)
    
    def get_task_by_id(self, task_id):
        tests = self.tests[self.tests.task_id == task_id]
        solutions = self.solutions[self.solutions.task_id == task_id]
        return Task(tests, solutions, self.tasks[self.tasks['id'] == task_id])

if __name__ == "__main__":
    dm = DataManager('train')
    task = dm.get_task(4)
    print(task.desription)
    test = task.get_test(0)
    print(test)