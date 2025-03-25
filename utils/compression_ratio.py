from collections import Counter

class compression_ratio:
    def solution(self,original_corpus: Counter, corpus: Counter):
        '''
        计算压缩率
        '''
        utf8_size = 0
        for word, freq in original_corpus.items():
            # utf8编码的长度, 注意这里我们把</w>也计算在内
            utf8_size += len(word.split()) * freq
        bpe_size = 0
        for word, freq in corpus.items():
            # bpe编码的长度
            bpe_size += len(word.split()) * freq
        return utf8_size / bpe_size
    
def main():
    original_corpus = {
        'l o w e s t </w>': 2,
    }
    corpus = {
        'l o w est </w>': 2,
    }
    compression_ratio_instance = compression_ratio()
    ratio = compression_ratio_instance.solution(original_corpus, corpus)
    print('compression ratio:', ratio)

if __name__ == '__main__':
    main()

