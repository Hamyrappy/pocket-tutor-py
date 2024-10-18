from typing import Callable

import pandas as pd
import torch
from transformers import BertModel, BertTokenizer
import json

print("Loading models...", end="")
model_name = "DeepPavlov/rubert-base-cased-sentence"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)
print("OK")


def get_sentence_embedding(sentence: str) -> torch.Tensor:
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        embedding = outputs.last_hidden_state[:, 0, :].squeeze()
    return embedding


def string2embedding(string: str) -> torch.Tensor:
    return torch.Tensor([float(i) for i in string.split()])


def embedding2string(embedding: torch.Tensor) -> str:
    return " ".join([str(i) for i in embedding.tolist()])


def generate_submit(test_solutions_path: str, predict_func: Callable, save_path: str, use_tqdm: bool = True, save_intermediate: bool = False, startfrom: int = 0, data_type = 'test') -> None:
    test_solutions = pd.read_excel(test_solutions_path)
    bar = range(startfrom, len(test_solutions))
    if use_tqdm:
        import tqdm

        bar = tqdm.tqdm(bar, desc="Predicting")

    submit_df = pd.DataFrame(columns=["solution_id", "author_comment", "author_comment_embedding"])
    if save_intermediate:
        intermediate = []
    for i in bar:
        
        solution_row = test_solutions.iloc[i]
        idx = str(solution_row["id"])
        if save_intermediate:
            text, analysis_result = predict_func(idx, return_analysis=True)
        else:
            text = predict_func(idx)
        embedding = embedding2string(get_sentence_embedding(text))
        submit_df.loc[i] = [idx, text, embedding]
        with open(f'logs/{data_type}{i}.json', 'w', encoding='utf-8') as f:
                json.dump([idx, text, embedding], f, ensure_ascii=False)
        if save_intermediate:
            intermediate.append({'question':analysis_result, 'answer': solution_row['author_comment']})
            with open(f'logs/{data_type}{i}_i.json', 'w', encoding='utf-8') as f:
                json.dump({'question':analysis_result, 'answer': solution_row['author_comment']}, f, ensure_ascii=False)
            
    submit_df.to_csv(save_path, index=False)
    if save_intermediate:
        json.dump(intermediate, open("intermediate.json", "w", encoding='utf-8'), ensure_ascii=False)