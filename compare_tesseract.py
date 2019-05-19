import os
import argparse
import codecs
import time

from tesserocr import PyTessBaseAPI, OEM

import torch
from torch.utils.data import Dataset

import torchvision.transforms.functional as TF

from PIL import Image

import data
import model
import accuracy


parser = argparse.ArgumentParser(description='Compare to Tesseract OCR')
parser.add_argument('-m', '--model', metavar='m', type=str, default='model.pth')
parser.add_argument('input_dir', type=str, help='Input directory')

args = parser.parse_args()

device = torch.device('cpu')

dataset = data.MyDataset(args.input_dir)

net = model.MyNet().to(device)
net.load_state_dict(torch.load(args.model, map_location='cpu'))
net.eval()
torch.no_grad()

time_sum_tess = 0
time_sum_mynet = 0

accuracy_sum_tess = 0.0
accuracy_sum_mynet = 0.0

accuracy_worst_tess = float('inf')
accuracy_worst_mynet = float('inf')

num_total = 0

with PyTessBaseAPI(lang='rus', oem=OEM.LSTM_ONLY) as api:
    for i in range(len(dataset)):
        num_total += 1
        img, target_as_numbers, _ = dataset[i]
        target = data.numbers_to_text(target_as_numbers).strip()
        pil_img = TF.to_pil_image(img, mode='L')

        start_time = time.perf_counter()
        
        api.SetImage(pil_img)
        tess_text = api.GetUTF8Text().strip()
        
        time_sum_tess += time.perf_counter() - start_time
        accuracy_tess = accuracy.accuracy(tess_text, target)        
        accuracy_sum_tess += accuracy_tess
        accuracy_worst_tess = min(accuracy_tess, accuracy_worst_tess)

        start_time = time.perf_counter()

        img = img.to(device)
        my_result_batch = net(torch.unsqueeze(img, dim=0))
        my_result_batch = my_result_batch.permute(1, 0, 2)
        my_text = data.decode_batch(my_result_batch)[0]

        time_sum_mynet += time.perf_counter() - start_time
        accuracy_mynet = accuracy.accuracy(my_text, target)
        accuracy_sum_mynet += accuracy_mynet
        accuracy_worst_mynet = min(accuracy_mynet, accuracy_worst_mynet)

        if i % 20 == 0:
            print('\r', '%s / %s' % (i, len(dataset)), end="")

print()                
print("Tesseract average accuracy:", accuracy_sum_tess / num_total)
print("Tesseract average time:", time_sum_tess / num_total)
print("Tesseract worst accuracy:", accuracy_worst_tess)

print("MyNet average accuracy:", accuracy_sum_mynet / num_total)
print("MyNet average time:", time_sum_mynet / num_total)
print("Mynet worst accuracy:", accuracy_worst_mynet)
