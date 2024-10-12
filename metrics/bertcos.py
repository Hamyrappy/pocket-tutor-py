'''cosine similarity between BERT-generated embeddings'''
from transformers import BertModel, BertTokenizer
import torch
import numpy as np
import warnings
warnings.filterwarnings("ignore")


def wrap(x, tp = torch.tensor):
    '''wraps x into iterable'''
    if isinstance(x, list) or isinstance(x, tuple) or isinstance(x, np.ndarray) or isinstance(x, torch.Tensor):
        return x
    else:
        return tp([x])

class BertCos():
    def __init__(self, model_name):
        '''
        Currenly supports only BERT, not DistilBERT
        Args:
            model_name: name of the BERT model to use
            tokenizer: tokenizer to use (default is BertTokenizer)
        Raises:
            ValueError: if model name is not recognized
        '''
        if model_name.startswith('bert'):
            self.model= BertModel.from_pretrained(model_name)
            self.tokenizer = BertTokenizer.from_pretrained(model_name)
        else:
            raise ValueError('Wrong model name')
    
    def pad_texts(self, x, y):
        '''Pads sentences to the same length'''
        xy = torch.nn.utils.rnn.pad_sequence(x + y, batch_first=True, padding_value = 0)
        x, y = xy[:len(x)], xy[len(x):]
        mask_x = torch.where(x != 0, 1, 0)
        mask_y = torch.where(y != 0, 1, 0)
        return x, y, mask_x, mask_y
    
    def __call__(self, x, y):
        '''
        Computes cosine similarity between two sentences using BERT-generated embeddings.
        Args:
            x (str): First sentence
            y (str): Second sentence
        Returns:
            cosine similarity between two sentences'''
        x = wrap(x, tp = list)
        y = wrap(y, tp = list)
        x = [torch.tensor(self.tokenizer.encode(x_, add_special_tokens=True)) for x_ in x]
        y = [torch.tensor(self.tokenizer.encode(y_, add_special_tokens=True)) for y_ in y]
        x, y, mask_x, mask_y = self.pad_texts(x, y)
        x = self.model(x, attention_mask = mask_x)[0].sum(dim=2)
        y = self.model(y, attention_mask = mask_y)[0].sum(dim=2)
        return torch.nn.functional.cosine_similarity(x, y)
