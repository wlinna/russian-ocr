#!/usr/bin/env python
# coding: utf-8

# In[1]:


import unicodedata
import collections
import random

from matplotlib.pyplot import imshow
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

import PIL

get_ipython().run_line_magic('matplotlib', 'inline')

PIL.PILLOW_VERSION


# In[2]:


RUS_LETTERS = 'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя'
NUMBERS = '0123456789'
PUNCTUATION_MARKS = ' .,?:;—!<>-«»()[]*"'
ALL_SYMBOLS = RUS_LETTERS + NUMBERS + PUNCTUATION_MARKS


# In[7]:


#data0 = open('../russian_news_corpus/russian_news_edit_25.txt', 'r')
data0 = open('test_w25.txt', 'r')

LIMIT = 100000
START = 0


# In[8]:


"""
counter = collections.Counter(''.join(data0))
print(''.join([k for k in counter.keys() if k not in RUS_LETTERS and k not in NUMBERS]))
sum(counter.values())
data0.index(max(data0, key=len))
len(max(data0, key=len))
"""


font = ImageFont.truetype('Roboto-Regular.ttf', 20)
"""
max_width = 0
max_height = 0
max_width_i = 0

for i, line in enumerate(data0):
    
    if i < START: continue
    if i > LIMIT: break

    line = line.upper()
    size = font.getsize(line)
    
    if size[0] >  max_width:
        max_width = size[0]
        max_width_i = i

    max_height = max(size[1], max_height)
    
print(max_width_i, max_width, max_height)
#counter
#[(l, l in counter) for l in RUS_LETTERS]
#[(l, l in counter) for l in '0123456789–']
"""


# In[9]:


save_path = Path('..') / 'lines_test_w25'

WIDTH = 340
for i, line in enumerate(data0):
    # We don't have much disk space

    if i < START: continue
    if i > LIMIT: break
    
    w = random.randint(200, 255)
    b = random.randint(0, 100)
    
    img = Image.new('L', (WIDTH, 32), color = (w,))
    drawing = ImageDraw.Draw(img)
    drawing.text((5, 5), line, font=font, fill=(b, ))
    img.save(save_path / ('%s_a.png' % i))
    with open(save_path / ('%s_a.gt.txt' % i), 'w') as f: f.write(line)
        
    line = line.upper()
    img = Image.new('L', (WIDTH, 32), color = (w, ))
    drawing = ImageDraw.Draw(img)
    drawing.text((5, 5), line, font=font, fill=(b,))
    img.save(save_path / ('%s_b.png' % i))
    with open(save_path / ('%s_b.gt.txt' % i), 'w') as f: f.write(line)
       
    """
    size = font.getsize(line)
    max_width = max(max_width, size[0])
    max_height = max(max_height, size[1])
    """
    


# In[6]:


print(max_width, max_height)

