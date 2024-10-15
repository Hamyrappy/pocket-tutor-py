from tester import Tester
from datamanager import DataManager

dm = DataManager('test')

task = dm.get_task(21)
code = task.author_solution
tester = Tester(task)
for i, result in enumerate(tester.evaluate(code, author_solution=True)):
    if not result[0]:
        #print('{}\n{}\n{}'.format(task.pre, code, task.post))
        print(i, result[1])
        break
else:
    print('correct')
'''for i in range(dm.get_num_tasks()):
    task = dm.get_task(i)
    code = task.author_solution
    tester = Tester(task)
    for result in tester.evaluate(code, author_solution=True):
        if not result[0]:
            print(i, task.id)
            break'''
    