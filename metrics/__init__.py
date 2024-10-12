'''Metrics to be used in the project'''

from .bertcos import BertCos

bertcos = BertCos('bert-base-multilingual-cased').__call__