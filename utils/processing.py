import pandas as pd
import re
import json

def remove_error_message(text):
    pattern = r"Ошибка в ((открытых и скрытых)|(скрытых и открытых)|открытых|скрытых) тестах"
    return re.sub(pattern, "", text).strip()


def clean_author_comment(data: pd.DataFrame):
    """
    Обработка через regex плашек в
    комментариях учителя

    Input:
        pd.DataFrame из файла ../train/solutions.xlxs
    Output:
        тот же pd.DataFrame с очищенными комментариями
        на основе заданных правил
    """

    data_regex = data.copy()

    data_regex["author_comment"] = data_regex["author_comment"].apply(
        remove_error_message
    )
    return data_regex

def _predict_error_message(row):
    if not row['syntax_error']:
        if row['error_on_closed'] and row['error_on_open']:
            return "Ошибка в открытых и скрытых тестах. "
        if row['error_on_closed']:
            return "Ошибка в скрытых тестах. "
        if row['error_on_open']:
            return "Ошибка в открытых тестах. "
    
    return ''
    

def predict_error_message(json_data):

    for key, value in json_data.items():
        value['error_message'] = _predict_error_message(value)
        value.pop('error_on_closed')
        value.pop('error_on_open')
        value.pop('syntax_error')
    
    return json_data

def remove_comments_and_docstrings(code):
    def remove_comments(text):
        # Удаляем однострочные комментарии
        text = re.sub(r'(?<!\\)#.*$', '', text, flags=re.MULTILINE)
        return text.strip()

    # Удаляем docstrings
    code = re.sub(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', '', code)
    
    # Обрабатываем код построчно
    lines = code.split('\n')
    result_lines = []
    in_string = False
    string_char = None

    for line in lines:
        new_line = ""
        i = 0
        while i < len(line):
            if not in_string:
                if line[i:i+3] in ['"""', "'''"]:
                    i += 3
                elif line[i] in ['"', "'"]:
                    in_string = True
                    string_char = line[i]
                    new_line += line[i]
                elif line[i] == '#':
                    break
                else:
                    new_line += line[i]
            else:
                if line[i:i+len(string_char)] == string_char and line[i-1] != '\\':
                    in_string = False
                    new_line += string_char
                    i += len(string_char) - 1
                else:
                    new_line += line[i]
            i += 1
        
        if new_line.strip():
            result_lines.append(new_line.rstrip())

    return '\n'.join(result_lines)
