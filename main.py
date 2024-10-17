import os

import pandas as pd
from agentic_system import AngenticSystem
from app.utils.submit import generate_submit
import json
from scripts.run_tester import run_tester

if __name__ == "__main__":
    run_tester() #-- для запуска тестировщика. Работает долго, запускайте один раз. Уже выполнен.
    data = json.load(open("data/processed/test/prepared.json", "r", encoding="utf-8"))
    ag_sys = AngenticSystem(os.environ["SAMBANOVA_API_KEY"])

    def predict(row: pd.Series):
        solution_id = row['id']
        info = data[str(solution_id)]
        model_output = ag_sys.predict(**info)
        return model_output
        


    generate_submit(
        test_solutions_path="data/processed/test/solutions.xlsx",
        predict_func=predict,
        save_path="data/complete/submission.csv",
        use_tqdm=True,
    )
