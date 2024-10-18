'''На случай если во время выполнения модель крашнулась и нужно воссоздать результат работы по логам'''


import json
import pandas as pd
data_type = 'test'
try:
    submit_df = pd.DataFrame(columns=["solution_id", "author_comment", "author_comment_embedding"])
    i = 0
    while True:
        i+=1
        
        submit_df.loc[i] = json.load(open(f'logs/{data_type}{i}.json', 'r', encoding='utf-8'))
    
except FileNotFoundError:
    submit_df.to_csv('data/complete/submissions_merged.csv', index=False)