# -*- coding: utf8 -*-
# extractor.py
# Entities extraction class
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

import traceback
from feet.utils.logger import LoggingMixin
from feet.utils.decorators import timeout, timeit, memoized
from feet.config import settings
from feet.entities.nlp import Parser


class Extractor(LoggingMixin):
    def __init__(self,
                 ref_dictionary,
                 grammar=None):
        if grammar is None:
            self._grammar = 'NE : {<NNP|NNPS|NN>*<DT>?<NNP|NNPS|JJ|NNS|NN>+}'
        else:
            self._grammar = grammar
        self._ref_dictionary = ref_dictionary

    @memoized
    def parser(self):
        return Parser('en')

    @timeit
    @timeout(settings.timeout)
    def extract(self, text, lang=None):
        """
        Extract entities from a text
        """
        res = self.parser.extract_entities(text, self._grammar, lang)
        chunks = res[0][0]
        output = []
        self.logger.debug('lang: %s' % lang)
        self.logger.debug('chunks: %s' %
                          ','.join([c.decode('utf8') for c in chunks]))
        if len(chunks) >= 1:
            for idx, chunk in enumerate(chunks):
                entities, not_entity =\
                    self.lookup(chunk, lang)
                self.logger.debug('selection: %s' % entities)
                add_new_variant, entity_found, add_new_entity = 0, 0, 0
                if len(entities) > 0 and not_entity == []:
                    entity_found = 1
                elif len(not_entity) > 0 and len(list(entities)) == 0:
                    add_new_entity = 1
                elif len(not_entity) > 0 and len(list(entities)) > 0:
                    entity_found, add_new_variant = 1, 1
                if len(not_entity) > 0 or len(list(entities)) > 0:
                    output.append({"position": idx,
                                   "chunk": chunk,
                                   "new_variant": not_entity,
                                   "add_new_variant": add_new_variant,
                                   "entity_found": entity_found,
                                   "entity_candidates": list(entities),
                                   "add_new_entity": add_new_entity})

            return output
        else:
            return []

    def lookup(self, chunk, text_lang):
        """
        Look for best candidates of entities in a dictionary
        """
        tokens, index, entity_options_list, not_an_entity = \
            [], 0, [], []
        self.logger.debug('chunk: %s' % chunk)
        # TODO: make a decision here to enforce or not enforce
        # the language of document compated to the language of
        # chunk
        if self._ref_dictionary.exact_match(chunk, text_lang):
            self.logger.debug('\texact match %s' % chunk)
            return set([chunk]), not_an_entity
        tokens = self.parser.word_tokenize(chunk, text_lang)
        self.logger.debug('\tchunk tokens:%s', ','.join(tokens))
        while index < len(tokens):
            try:
                self.logger.debug('\tchunk token: %s', tokens[index])
                res = self._ref_dictionary.candidates(tokens[index],
                                                      text_lang)
                entities = res
                self.logger.debug('\t\tchunk token candidates: %s' %
                                  ','.join(entities))
                if entities != set([]):
                    entities = self.select_best_choice(
                        tokens,
                        entities,
                        text_lang
                    )
                    if len(entities) > 0:
                        entity_options_list.append(entities)
                    else:
                        not_an_entity.append(tokens[index])
            except:
                self.logger.error(traceback.format_exc())
            finally:
                index += 1
                self.logger.debug('options list: %s' % entity_options_list)
        return self.intersection(entity_options_list), not_an_entity

    def select_best_choice(self, chunk_tokens, choices, chunk_lang):
        """
        let's see the proportion of tokens that are common between considered
        choices and found choices. We want a minimum of 2/3 tokens in common.
        """
        output = []
        for candidate in choices:
            self.logger.debug('\tcandidate:%s' % candidate)
            tokens = self._ref_dictionary.tokens(candidate, chunk_lang)
            self.logger.debug('\tcandidate tokens:%s' % ','.join(tokens))
            res = set.intersection(set(tokens), set(chunk_tokens))
            if len(tokens) != 0:
                ratio = float(len(res)) / float(len(tokens))
            else:
                ratio = 0
            self.logger.debug('\t\tratio:%f' % ratio)
            if ratio > 2.0 / 3.0:
                output.append(candidate)
        return output

    def intersection(self, options_lists):
        """
        Get intersection of lists of candidates for entities
        """
        entities_set = [set(sub_list) for sub_list in options_lists]
        try:
            intersection_set = set.intersection(*entities_set)
            if not intersection_set:
                return []
        except:
            intersection_set = set([])
        return list(intersection_set)
