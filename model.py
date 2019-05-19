import torch

import torch.nn as nn
import torch.nn.functional as F

from data import SYMBOL_SET


_CNN_OUT_CHANS = 60
class MyNet(nn.Module):
    def __init__(self):
        super(MyNet, self).__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(1, 40, 3, padding=1),
            nn.MaxPool2d(2),
            nn.ReLU(),
            nn.Conv2d(40, _CNN_OUT_CHANS, 3, padding=1),
            nn.MaxPool2d(2),
            nn.ReLU(),            
        ) 

        self.avgpool = nn.AdaptiveAvgPool2d((1, None))

        self.classifier = nn.Linear(_CNN_OUT_CHANS, len(SYMBOL_SET))
        self.log_softmax = nn.LogSoftmax(dim=2)

        
    def forward(self, x):
        # The image size in training: 340 x 32
        # [B, Cin, Hin, Win]:     [B, 1, 32, 340]
        x = self.conv(x)    #     [B, 60, 8, 85]
        x = self.avgpool(x) #     [B, 60, 1, 85]

        # Reshape to the format expected by a Linear layer : [B, *, features]
        x = x.permute(0, 3, 1, 2).view(x.size(0), x.size(3), -1)
        
        x = self.classifier(x) #  [B, seq_len (85), features = |symbol_set|]
        # log_softmax expects inputs in the following shape
        x = x.permute(1, 0, 2) #  [seq_len (85), B, features = |symbol_set|]
        x = self.log_softmax(x)
        return x