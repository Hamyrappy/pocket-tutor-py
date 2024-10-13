import torch

class Model(torch.nn.Module):
    def __init__(self, mod) -> None:
        super().__init__()