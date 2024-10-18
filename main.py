import os

import pandas as pd
from agentic_system import AngenticSystem
from app.utils.submit import generate_submit
import json
from scripts.run_tester import run_tester

from utils.processing import predict_error_message
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv('env.env')
    #run_tester() #-- для запуска тестировщика. Работает долго, запускайте один раз. Уже выполнен.
    data_no_error_msgs = json.load(open("data/processed/test/prepared.json", "r", encoding="utf-8"))
    data = predict_error_message(data_no_error_msgs)

    ag_sys = AngenticSystem(os.environ["SAMBANOVA_API_KEY"], comment_writer_model_params={
        'model_name':'langchain'
    })
    def predict(idx):
        info = data[idx]
        model_output = ag_sys.predict(**info)
        return model_output
        


    generate_submit(
        test_solutions_path="data/processed/test/solutions.xlsx",
        predict_func=predict,
        save_path="data/complete/submission.csv",
        use_tqdm=True,
    )
