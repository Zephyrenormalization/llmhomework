import re,os
from collections import Counter
from typing import List, Tuple

class bpe:
    def __init__(self, path: str, vocab_size: int):
        '''
        arguments:
        original_corpus: dict, original corpus
        corpus: dict, bpe循环中的corpus
        vocab: set, bpe循环中的需要维护的词表，用于判断循环结束
        '''
        self.original_corpus = {}
        self.corpus = {}
        self.vocab = {}
        self.vocab_size = vocab_size
        with open(path, 'r', encoding='utf-8') as f:
            words = [' '.join(list(word)) + ' </w>' for line in f for word in line.strip().split()]
            self.original_corpus = Counter(words)
            self.corpus = self.original_corpus.copy()

    def get_pair_stats(self) -> Tuple[Tuple[str, str], int]:
        '''
        从corpus中获取pair的统计信息
        '''
        pairs = Counter()
        for word, freq in self.corpus.items():
            symbols = word.split()
            for i in range(len(symbols) - 1):
                pairs[(symbols[i], symbols[i + 1])] += freq
        return pairs
    
    def merge_vocab(self, pairs):
        '''
        将pair合并到vocab中
        '''
        pair = pairs.most_common(1)[0][0]
        new_corpus = Counter()
        # 待替换的模式串
        pattern = re.escape(' '.join(pair))
        # 替换后的串
        replacement = ''.join(pair)
        for word in self.corpus:
            new_word = re.sub(pattern, replacement, word)
            new_corpus[new_word] = self.corpus[word]
        self.corpus = new_corpus
        
    def update_vocab(self):
        '''
        更新vocab
        '''
        vocab = set()
        for word in self.corpus:
            symbols = word.split()
            for symbol in symbols:
                vocab.add(symbol)
        self.vocab = vocab

    def solution(self):
        '''
        bpe算法主循环
        '''
        while self.vocab_size > len(self.vocab):
            pairs = self.get_pair_stats()
            self.merge_vocab(pairs)
            self.update_vocab()
        return self.corpus, self.vocab
    
    def save(self, dir: str):
        '''
        保存vocab
        '''
        path = dir + f'/vocab_{self.vocab_size}.txt'
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(path, 'w', encoding='utf-8') as f:
            for word in self.vocab:
                f.write(word + '\n')
    
def main():
    path = './data/training-monolingual/news-commentary-v6.en'
    vocab_size = 1000
    bpe_instance = bpe(path, vocab_size)
    corpus, vocab = bpe_instance.solution()
    vocab = list(vocab)
    print('vocab size:', len(vocab))
    print(vocab[:10])
    print('-------------------')
    print('after bpe, corpus:')
    words = list(corpus)
    print(words[:10])

if __name__ == '__main__':
    main()