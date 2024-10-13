code = '''language = input() 

count_list = []
for key, value in interpreter.items():
    for k, v in value.items():
        if language not in v:
            count_list.append(k.split()[0].upper())
    
print(*count_list)'''

from tester import Tester
from datamanager import DataManager

dm = DataManager('train')
task = dm.get_task(4)

tester = Tester(task)
print(tester.evaluate(code))