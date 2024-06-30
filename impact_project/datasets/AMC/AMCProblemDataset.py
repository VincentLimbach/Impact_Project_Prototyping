import json
import os
import torch
from torch.utils.data import Dataset
from impact_project.datasets.utils import extensive_split

class AMCProblemDataset(Dataset):
    def __init__(self, json_file):
        """
        Args:
            json_file (string): Path to the json file with annotations.
        """
        with open(json_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.answer_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        
        problem = self.data[idx]
        
        text_data = problem['Setup'] + ' ' + problem['Options']
        
        answer_value = self.answer_map[problem['Answer'][0]]

        return {'data': text_data, 'value': answer_value}

    def get_corpus(self):
        all_text = ''
        for i in range(len(self.data)):
            item = self[i]
            all_text += ' ' + item['data']

        return extensive_split(all_text)
