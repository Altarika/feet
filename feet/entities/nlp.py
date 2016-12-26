# -*- coding: utf8 -*-
# Parser class: provides NLP tools
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

from nltk import word_tokenize, sent_tokenize, ne_chunk, \
    RegexpParser, pos_tag
from nltk.tree import Tree
from collections import defaultdict
from langdetect import detect_langs
from jptools import JAParser
from feet.utils.logger import LoggingMixin
from feet.utils.decorators import timeit
import traceback

WORLD_2_NLTK = {
    'english': 'english',
    'en': 'english',
    'fr': 'french',
    'french': 'french',
    'ja': 'japanese',
    'japanese': 'japanese'
}


class Parser(LoggingMixin):
    """
    Provides NLP tools such as language detection, tokenizer and POS tagger
    for entities
    """
    _auto_lang_detect = False
    _lang = 'en'

    def __init__(self, lang='english', auto_lang_detect=False):
        """
        Parser class initialisation.
        Defines a default language attribute and decides if automatic language
        detection is turned on/off.
        """
        self._auto_lang_detect = auto_lang_detect
        self._lang = WORLD_2_NLTK[lang]

    def detect_language(self, text):
        """
        Provides language detection of a text.
        Fallbacks to default language defined in class initialization or 'en'
        """
        try:
            if text is None:
                return None
            languages = detect_langs(text.decode('utf8'))
            if len(languages) > 0:
                return languages[0].lang
        except:
            self.logger.warning(traceback.format_exc())
            return self._lang or 'en'

    def word_tokenize(self, text, lang=None):
        """
        Tokenizes a sentence.
        """
        if lang is not None:
            lang = WORLD_2_NLTK[lang]
        else:
            lang = self._lang
        if lang == 'japanese':
            return JAParser().word_tokenize(text)
        else:
            if not isinstance(text, unicode):
                text = text.decode('utf8')
            return [token.encode('utf8')
                    for token in word_tokenize(text, lang)]
            # return text.split()

    def sent_tokenize(self, text, lang=None):
        """
        Splits a text into sentences. Yields each sentence for processing.
        """
        if lang is not None:
            lang = WORLD_2_NLTK[lang]
        else:
            lang = self._lang
        if lang == 'japanese':
            for sentence in JAParser().sent_tokenize(text):
                yield sentence
        else:
            if not isinstance(text, unicode):
                text = text.decode('utf8')
            for sentence in sent_tokenize(text, lang):
                yield sentence

    @timeit
    def tokenize(self, text, lang=None):
        """
        Tokenizes a text by splitting it into sentences that will be tokenized.
        """
        if lang is not None:
            lang = WORLD_2_NLTK[lang]
        else:
            lang = self._lang
        output = []
        if text is None:
            return output
        for sentence in self.sent_tokenize(text, lang):
            output.append(self.word_tokenize(sentence, lang))
        return output

    def _select_entities(self,
                         tree,
                         extra_classes=['NNP', 'NNPS', 'NN', 'NNS']):
        """
        Selects candidates of entities as chunks with specific grammatic tags.
        """
        entities = defaultdict(list)
        for chunk in tree:
            if isinstance(chunk, Tree):
                entities[chunk._label].append(
                    " ".join([token[0] for token in chunk.leaves()]))
            else:
                if chunk[1] in extra_classes:
                    entities['noun_phrase_leave'].append(chunk[0])
        return [i for key, value in dict(entities).iteritems() for i in value]

    @timeit
    def extract_entities(self, text, grammar=None, lang=None):
        """
        Extract entities from text
        """
        entities = []
        if lang is None:
            lang = WORLD_2_NLTK[self.detect_language(text)]
        else:
            if lang in WORLD_2_NLTK.keys():
                lang = WORLD_2_NLTK[lang]
            else:
                lang = self._lang
        if lang == 'japanese':
            return JAParser().extract_entities(text), lang
        pos_sentences = [pos_tag(self.word_tokenize(sentence, lang=lang))
                         for sentence in self.sent_tokenize(text, lang=lang)]

        if grammar is not None:
            chunker = RegexpParser(grammar)
            for pos_sentence in pos_sentences:
                tree = chunker.parse(pos_sentence)
                self.logger.debug(tree)
                entities = entities + self._select_entities(tree)
        else:
            for pos_sentence in pos_sentences:
                tree = ne_chunk(pos_sentence, binary=False)
                self.logger.debug(tree)
                entities = entities + self._select_entities(tree)
        return entities, lang
