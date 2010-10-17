#!/usr/bin/python
import nltk.corpus
import nltk.tag
import nltk.chunk
import itertools

class TagChunker(nltk.chunk.ChunkParserI):
    def __init__(self, chunk_tagger):
        self._chunk_tagger = chunk_tagger

    def parse(self, tokens):
        # split words and part of speech tags
        (words, tags) = zip(*tokens)
        # get IOB chunk tags
        chunks = self._chunk_tagger.tag(tags)
        # join words with chunk tags
        wtc = itertools.izip(words, chunks)
        # w = word, t = part-of-speech tag, c = chunk tag
        lines = [' '.join([w, t, c]) for (w, (t, c)) in wtc if c]
        # create tree from conll formatted chunk lines
        return nltk.chunk.conllstr2tree('\n'.join(lines))



def conll_tag_chunks(chunk_sents):
    tag_sents = [nltk.chunk.tree2conlltags(tree) for tree in chunk_sents]
    return [[(t, c) for (w, t, c) in chunk_tags] for chunk_tags in tag_sents]

def ubt_conll_chunk_train(train_sents):
    train_chunks = conll_tag_chunks(train_sents)

    u_chunker = nltk.tag.UnigramTagger(train_chunks)
    ub_chunker = nltk.tag.BigramTagger(train_chunks, backoff=u_chunker)
    ubt_chunker = nltk.tag.TrigramTagger(train_chunks, backoff=ub_chunker)
    ut_chunker = nltk.tag.TrigramTagger(train_chunks, backoff=u_chunker)
    utb_chunker = nltk.tag.BigramTagger(train_chunks, backoff=ut_chunker)
    
    return utb_chunker

conll_train = nltk.corpus.conll2000.chunked_sents('train.txt')
