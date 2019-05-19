import codecs

RUS_LETTERS = 'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя'
NUMBERS = '0123456789'
PUNCTUATION_MARKS = ' .,?:;—!<>-«»()[]*"'
ALL_SYMBOLS = PUNCTUATION_MARKS + NUMBERS + RUS_LETTERS

WIDTH = 25

def good_symbol(s): return s in ALL_SYMBOLS

def chunk_line(input, max_len):
    return (input[i:(i + max_len)] for i in range(0, len(input), max_len))

with codecs.open('russian_news.txt', 'r', 'utf-8', 'ignore') as f:
    out = open('russian_news_edit_%s.txt' % WIDTH, 'w')
    for line in f:
        line = ''.join(filter(good_symbol, line))
        for chunk in chunk_line(line, WIDTH):
            out.write(chunk.strip() + '\n')

    out.close()

