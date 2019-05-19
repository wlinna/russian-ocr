import os

import numpy as np
from skimage import io

import torch
from torch.utils.data import Dataset

# A special whitespace symbol. NOTE: this is a special kind of whitespace. It
# represents the whitespace between two consecutive letters, while normal
# space character represent a space of width 1.
# 'в^о' => 'во', but 'в о' => 'в о' 
WS_SYMBOL = '^'
SYMBOL_SET = WS_SYMBOL + ' .,?:;—!<>-«»()[]*"АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя0123456789'
WIDTH = 25
WS_CODE = SYMBOL_SET.index(WS_SYMBOL)

def text_to_numbers(text: str) -> np.array:
    return np.array([SYMBOL_SET.index(c) for c in text], dtype=np.int64)

def numbers_to_text(arr) -> str:
    return ''.join([SYMBOL_SET[code] for code in arr])

def decode_sequence(seq):
    out = []
            
    current_code = None
    for i, v in enumerate(seq):
        if v == current_code:            
            continue

        current_code = v
        if v == WS_CODE:
            current_code = None
            continue
                    
        out.append(v)

    return ''.join(numbers_to_text(out))

def _test_decode_sequence(input, expected):
    numbers = text_to_numbers(input)
    result = decode_sequence(numbers)
    assert result == expected, "%s == %s" % (result, expected)

_test_decode_sequence('аа^аа', 'аа')
_test_decode_sequence('  я^в^е^р^т^у ^^ ', ' яверту  ')

def decode_batch(input):
    """
    input in shape: [B, seq, feature]
    """

    # From the last dimension, choose the indices with highest
    # probabilities. These indices point to SYMBOL_SET
    maxed = torch.argmax(input.cpu(), -1).numpy()
    # [B, seq] : each value is an index to SYMBOL_SET
    return [decode_sequence(seq) for seq in maxed]
    
def load_image(path: str):
    img = io.imread(path)
    img = torch.from_numpy(img).view(1, 32, -1).float()
    return img

class MyDataset(Dataset):
    def __init__(self, data_path):
        self.data_path = data_path
        # Yes, all samples must be PNG files
        self.sample_ids = [f[:(f.rindex('.'))] for f in os.listdir(data_path) if f.endswith('.png')]
    
    def __len__(self):
        return len(self.sample_ids)
    
    def __getitem__(self, i):
        sample_path = self.data_path + '/' + self.sample_ids[i] 
        img = load_image(sample_path + '.png')
        with open(sample_path + '.gt.txt') as f:
            label = f.read().strip('\n')
            missing_chars = WIDTH - len(label)
            if missing_chars > 0:
                label += ' ' * missing_chars
        
        return (img, text_to_numbers(label), len(label)) 
