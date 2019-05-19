import argparse
import torch

import data
import model


parser = argparse.ArgumentParser(description='Recognize characters in a picture')
parser.add_argument('-m', '--model', metavar='m', type=str, default='model.pth')
parser.add_argument('input_image', type=str, help='Input image')
args = parser.parse_args()

device = torch.device('cpu')

net = model.MyNet().to(device)
net.load_state_dict(torch.load(args.model, map_location='cpu'))
net.eval()

img = data.load_image(args.input_image).to(device)
img = torch.unsqueeze(img, dim=0)
result_batch = net(img).permute(1, 0, 2)
result = data.decode_batch(result_batch)[0]

print(result)