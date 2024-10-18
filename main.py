import os

import pandas as pd
from agentic_system import AngenticSystem
from app.utils.submit import generate_submit
from app.utils.metric import calculate_score
import json
from scripts.run_tester import run_tester

from utils.processing import predict_error_message
from dotenv import load_dotenv
import agentic_system.prompts as prompts
import time


if __name__ == "__main__":
    data_type = "test"
    
    save_path = "data/complete/submission.csv"
    
    load_dotenv('env.env')
    #run_tester() #-- для запуска тестировщика. Работает долго, запускайте один раз. Уже выполнен.
    data_no_error_msgs = json.load(open(f"data/processed/{data_type}/prepared.json", "r", encoding="utf-8"))
    data = predict_error_message(data_no_error_msgs)

    ag_sys = AngenticSystem(
        injection_checker_model_params={
        'model_name':'SambaNova',
        'model_params': {
            'base_url' : "https://api.sambanova.ai/v1/",  
            'api_key' : 'a2ba3807-4759-48ce-aa4d-8549541d3b4f',
            'streaming' : True,
            'model' : 'Meta-Llama-3.1-70B-Instruct'
        }, 
        'template' : prompts.injection_checker_template
        },
        jailguard_model_params={
        'model_name':'SambaNova',
        'model_params': {
            'base_url' : "https://api.sambanova.ai/v1/",  
            'api_key' : '0be10165-0ee8-4403-b53b-8399e968519e',
            'streaming' : True,
            'model' : 'Meta-Llama-3.1-70B-Instruct'
        },
        'template': prompts.jailguard_template
        },
        code_analysis_model_params={
        'model_name':'SambaNova',
        'model_params': {
            'base_url' : "https://api.sambanova.ai/v1/",  
            'api_key' : 'bb8e15ea-569a-4b42-ac98-39c6832167cc',
            'streaming' : True,
            'model' : 'Meta-Llama-3.1-70B-Instruct'
        },
        'template': prompts.code_analysis_template
        },
        
        comment_writer_model_params={
        'model_name':'YandexGPT',
        'model_params': {
            'IAM_token' : "t1.9euelZrOmJ7LmZmMi5zKisyRxo-Qje3rnpWax5LHysaPlJOXkMvNnZbJjpzl8_dpCjdH-e9OXQhz_t3z9yk5NEf5705dCHP-zef1656Vmo3MjJidkZrHl86Zy5bPlJiY7_zF656Vmo3MjJidkZrHl86Zy5bPlJiY.3ZaunjBvjweQIwQ_Ds4PYg1-WTygpRuphP2FHZY_Ndnn4qfk9ypvnSBQBxWb8aXF77-sSBvQsklOWPA3iYgGCA",
            'folder_id' : 'b1gi0bfnfat2dfgtf3uh',
            'model_type_or_id': 'bt193kh5joiibpj97h47',
            'system_prompt': prompts.YandexGPT_system_prompt
        },
        'template': prompts.comment_writer_template_no_comments,
        },
        need_comments = False, 
        required_sleep_time=1)
    def predict(idx, return_analysis = False):
        info = data[idx]
        model_output = ag_sys.predict(**info, return_analysis=return_analysis)
        return model_output
        


    generate_submit(
        test_solutions_path=f"data/processed/{data_type}/solutions.xlsx",
        predict_func=predict,
        save_path=save_path,
        use_tqdm=True, 
        save_intermediate = False
    )
    
    if data_type == "train":
        print('Score:', calculate_score(save_path, f"data/processed/{data_type}/solutions.xlsx"))
