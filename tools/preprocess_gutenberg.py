import argparse
import codecs

parser = argparse.ArgumentParser(description='Chunk text')
parser.add_argument('-w', '--width', metavar='w', type=int, default=25)
parser.add_argument('input', type=str, help='an integer for the accumulator')

args = parser.parse_args()

RUS_LETTERS = 'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя'
NUMBERS = '0123456789'
PUNCTUATION_MARKS = ' .,?:;—!<>-«»()[]*"'
ALL_SYMBOLS = PUNCTUATION_MARKS + NUMBERS + RUS_LETTERS

def good_symbol(s): return s in ALL_SYMBOLS

def chunk_line(input, max_len):
    return (input[i:(i + max_len)] for i in range(0, len(input), max_len))

with codecs.open(args.input, 'r', 'utf-8', 'ignore') as f:
    out_path = args.input.replace('.txt', '_w%s.txt' % args.width)
    out = open(out_path, 'w')
    for line in f:
        line = ''.join(filter(good_symbol, line))

        for chunk in chunk_line(line, args.width):
            stripped = chunk.strip()
            # To filter out lines with nothing but punctuantion marks
            if stripped.strip(PUNCTUATION_MARKS):
                out.write(stripped + '\n')

    out.close()

