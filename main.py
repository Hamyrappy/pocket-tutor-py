import os

import pandas as pd
from agentic_system import AngenticSystem
from app.utils.submit import generate_submit
import json
from scripts.run_tester import run_tester
from agentic_system.prompts import code_analysis_template_2, comment_writer_template_2

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
        
    #run_tester() #-- для запуска тестировщика. Работает долго, запускайте один раз. Уже выполнен.
    data = json.load(open("data/processed/test/prepared.json", "r", encoding="utf-8"))
    ag_sys = AngenticSystem(os.environ["SAMBANOVA_API_KEY"],comment_writer_template=comment_writer_template_2,code_analysis_template=code_analysis_template_2)

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
