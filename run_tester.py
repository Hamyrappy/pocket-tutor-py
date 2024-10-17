from utils import DataManager, Tester, add_anomaly
import json
datapath = 'data/processed/{}/prepared.json'

for data_type in ['train', 'test']:
    data = {}
    dm = DataManager('data/processed/{}'.format(data_type))

    for i in range(len(dm)):
        task = dm.get_task(i)
        tester = Tester(task)
        for solution in task.solutions:
            report_dict = solution.test(tester)
            report = report_dict['where_error']*report_dict['syntax_error']+report_dict['report']
            data[solution.id]={
                'student_solution' : solution.solution,
                'task': task.desription,
                'author_solution': task.author_solution,
                'test_system_report': report}
            if report_dict['correct']:
                add_anomaly({'type': 'Correct solution',
                             'about':{
                                 'data_type':data_type,
                                 'id':solution.id,
                                 'student_solution' : solution.solution,
                                 'task': task.desription,
                                 'task_id':task.id}})
            elif report_dict['correct'] is None:
                add_anomaly({'type': 'Missing files',
                             'about':{
                                 'data_type': data_type,
                                 'task': task.desription,
                                 'task_id': task.id,
                                 'comment': task.add}})
    json.dump(data, open(datapath.format(data_type), 'w', encoding='utf-8'), ensure_ascii=False)
            
