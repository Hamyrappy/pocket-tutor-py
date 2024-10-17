'''Tool to chek if all author solutions are considered correct by test system'''

from utils import Tester, DataManager

for data_type in ['train', 'test']:
    dm = DataManager('data/processed/{}'.format(data_type))

        task = dm.get_task(i)
        code = task.author_solution
        tester = Tester(task)
        for result in tester.test(code, author_solution=True):
            if not result[0]:
                print('Found a task where author solution is considered incorrect: task № {}, id {} from {} data'.format(i, task.id, data_type))
                break
    