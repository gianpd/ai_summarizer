import os
import sys
import logging
logging.basicConfig(stream=sys.stdout, format='%(asctime)-15s %(message)s',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger("Summarizer")
from functools import lru_cache

from typing import List, Dict

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest

from app.config import get_settings

from transformers import AutoTokenizer
from huggingface_hub.inference_api import InferenceApi

### instantiate the hugging face hub inference
# Config = get_settings()
# API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn" 
inference = InferenceApi(repo_id="facebook/bart-large-cnn", token=os.getenv('HF_TOKEN'))

# spacy nlp object
nlp = spacy.load("en_core_web_sm")

@lru_cache
def load_tokenizer(tokenizer_model: str = 'facebook/bart-large-mnli'):
    return AutoTokenizer.from_pretrained(tokenizer_model)

tokenizer = load_tokenizer()


def get_summaries_from_hf(text: str) -> str:
    """
    Get summaries from hf: first of all get nested sentences in order to be sure each text has a max number of 1024 tokens, then call hf api inference.
    
    --Parameters
     - text: (str) the string text to be summarized.

     return a string contained the total summary.

     """
    summaries = []
    str_chunks = get_nest_sentences(text, tokenizer)
    for i, str_chunk in enumerate(str_chunks):
        summary = inference(str_chunk)[0]['summary_text']
        logger.info(f"Retrived summary {i}: {summary}")
        summaries.append(summary)
    return ' '.join(summaries)


def get_significant_words_list(doc: spacy.tokens.doc.Doc) -> List[str]:
    """
    Get a list contained words that are important for the speech (PROPN; ADJ; NOUN; VERB): excluding stop words, punctations
    """
    words = []
    stopwords = list(STOP_WORDS)
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    for token in doc:
        if (token.text in stopwords or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag):
            words.append(token.text)
    return words

def get_frequency_words(words: List[str]) -> Counter:
    """Get a counter with the frequency of each word normalized to one."""
    freq_word = Counter(words)
    max_freq = freq_word.most_common(1)[0][1]
    for word in freq_word.keys():
        freq_word[word] = (freq_word[word] / max_freq)
    return freq_word

def get_sent_strenght(doc: spacy.tokens.doc.Doc, freq_word: Counter) -> Dict:
    """Get a dictionary where the keys are sentence (str) and the values are float indicating the importance score of the sentence, based on most high frequencies words."""
    sent_strenght = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strenght.keys():
                    sent_strenght[sent] += freq_word[word.text]
                else:
                    sent_strenght[sent] = freq_word[word.text]
    return sent_strenght


def deterministic_summary_pipeline(doc: str) -> str:
    """Get a final summary of a doc, using a number of top sentences."""
    doc = nlp(doc)
    n_sents = len(list(doc.sents))
    logger.info(f"Starting to compute summary from {n_sents} sentences ...")
    words = get_significant_words_list(doc)
    freq_word = get_frequency_words(words)
    sent_strenght = get_sent_strenght(doc, freq_word)
    
    n_sents = int(n_sents * 0.30) # use just the 30% of the sentences
    logger.info(f"Getting the {n_sents} largest sentences for the summary ...")
    summarized_sentences = [x.text for x in nlargest(n_sents, sent_strenght, key=sent_strenght.get)]

    summary = ''.join(summarized_sentences)

    start_sentence = list(doc.sents)[0].text

    if start_sentence in summarized_sentences:
        if summarized_sentences[0] == start_sentence:
            return summary
        else:
            start_idx = summarized_sentences.index(start_sentence)
            _ = summarized_sentences.pop(start_idx)
            # remove the start_idx element and return the total summary with start_sentence as first value
            return start_sentence + ' '.join(summarized_sentences)
    else:
        return start_sentence + summary



def get_nest_sentences(document: str, tokenizer: AutoTokenizer, token_max_length = 1024):
    """
    Starting from a large document, a list of sequential string is computed, such that each string has
    a number of tokens equal to token_max_length.

    ---Params
    - document: the long text (str)
    - tokenizer: the pre-trained tokenizer to be used.
    - token_max_length: the maximum number of token has required by the NLP model (int)
    """
    sents = []
    length = 0
    doc = nlp(document)
    s = ''
    for sentence in doc.sents:
        tokens_in_sentence = tokenizer(str(sentence), truncation=False, padding=False)[0]
        length += len(tokens_in_sentence) # how many tokens the current sentence have summed to the previous
        if length <= token_max_length:
            s += sentence.text
        else:
            sents.append(s)
            s = sentence.text
            length = 0
    # append last string with less # of tokens than token_max_length
    sents.append(s)
    logger.info(f'Returning {len(sents)} number of chunk strings')
    return sents