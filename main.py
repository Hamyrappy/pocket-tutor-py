import os

import pandas as pd
from models import *
from app.utils.submit import generate_submit
import json

if __name__ == "__main__":

    data = json.load(open("data/processed/test/prepared.json", "r"))
    librarian = Librarian(???)
    formatter = Formatter(???)
    commentator = Commentator(???)
    template = '''?????????????
УСЛОВИЕ ЗАДАЧИ:
{task}

ОБРАЗЕЦ правильного решения:
{correct_example}

НЕПРАВИЛЬНОЕ РЕШЕНИЕ ученика:
{student_solution}

ПРИМЕРЫ комментария:
1.
{comments[0]}

2.
{comments[1]}

3.
{comments[2]}

4.
{comments[3]}'''
    def predict(row: pd.Series) -> str:
        solution_id = row['id']
        info = data[str(solution_id)]
        task = info['task']
        student_solution = info['student_solution']
        author_solution = info['author_solution']
        test_system_report = info['test_system_report']
        other_comments = librarian(???)
        prompt = template.format(
            task=task,
            student_solution=student_solution,
            author_solution=author_solution,
            test_system_report=test_system_report,
            comments=other_comments
        )
        model_output_raw = commentator(prompt)
        model_output = formatter(model_output_raw)
        return model_output
        


    generate_submit(
        test_solutions_path="../data/raw/test/solutions.xlsx",
        predict_func=predict,
        save_path="../data/processed/submission.csv",
        use_tqdm=True,
    )
