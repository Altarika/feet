# -*- coding: utf8 -*-
# jptools
# Tools for NLP with Japanese Language
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

import MeCab
import re
from datetime import datetime
from feet.config import settings
from dateparser import parse
from feet.utils.decorators import memoized
from feet.utils.singleton import SingletonMetaClass
from feet.utils.logger import LoggingMixin
DATE_REGEX_FORMAT = [
    {
        'regex': ur'年[０-９]{2,2}月[０-９]{1,2}日[０-９]{1,2}',
        'format': '',
        'with_year': True
    },
    {
        'regex': ur'\d{1}月\d{1}日\（[一-龯]）〜\d{1}月\d{1}日\（[一-龯]）',
        'format': '',
        'with_year': False
    },
    {
        'regex': ur'\d{2,2}年\d{1,2}月\d{1,2}日',
        'format': '',
        'with_year': True
    },
    {
        'regex': ur'\d{4,4}年\d{1,2}月\d{1,2}日',
        'format': '',
        'with_year': True
    },
    {
        'regex': ur'\d{1,2}月\d{1,2}日',
        'format': '',
        'with_year': False
    },
    {
        'regex': ur'\d{1,4}/\d{1}/\d{1}',
        'format': '',
        'with_year': False
    },
    {
        'regex': ur'\d{1}/\d{1}',
        'format': '',
        'with_year': False
    }
]

F1_NOUN = '名詞'
F1_PARTICLE = '助詞'
F1_CONJONCTION = '接続詞'
F1_INTERJECTION = '感動詞'
F1_VERB = '動詞'
F1_AUXILIARY_VERB = '助動詞'
F1_ADJECTIVE = '形容詞'
F1_SEPARATOR = '記号'
F2_NUMBER = '数'
F2_SUFFIX = '接尾'
F2_SUFFIX_COUNTER = '接尾'
F2_IND_VERB = '自立'
F2_NO_MEANING_NAMES = '非自立'
F2_PRONOUN = '代名詞'
F2_ADVERBS = '副詞可能'
F2_ADJECTIVE = '形容動詞語幹'
F2_PROPER_NOUN = '固有名詞'
F3_ADVERBS = '副詞可能'
F3_SUFFIX_COUNTER = '助数詞'
SENTENCE_SEPARATORS = ('句点', '')
STOPLIST = set('http https for a of the and to in co com jp'.split())


class JAParser(LoggingMixin):
    __metaclass__ = SingletonMetaClass

    @memoized
    def mecab(self):
        self.logger.warning('Initialize Mecab')
        return MeCab.Tagger('-d %s' % settings.mecab.mecabdict)

    def word_tokenize(self, content, with_separators=True):
        if content is None:
            return None
        output = []
        node = self.mecab.parseToNode(content)
        while node:
            features = node.feature.split(',')
            self.logger.debug('%s %s %s' % (node.surface, features[0],
                                            features[1]))
            if node.surface != '':
                if features[0] == F1_SEPARATOR:
                    if with_separators:
                        output.append(node.surface)
                else:
                    output.append(node.surface)
            node = node.next
        return output

    def sent_tokenize(self, content):
        if content is None:
            return []
        node = self.mecab.parseToNode(content)
        separators = []
        while node:
            features = node.feature.split(',')
            self.logger.debug('%s %s %s' % (node.surface, features[0],
                                            features[1]))
            if node.surface == 'BOS/EOS' or (features[0] == F1_SEPARATOR and
                                             features[1] == '句点'):
                if node.surface != '':
                    separators.append(node.surface)
            node = node.next
        return filter(None, re.split(r"%s" % ('|'.join(separators)), content))

    def extract_entities(self, content, with_numbers=False):
        """
        Extract good candidates for entities in a text.
        """
        output = []
        node = self.mecab.parseToNode(content)
        sentence = 0
        entity = []
        while node:
            features = node.feature.split(',')
            f1 = features[0]
            f2 = features[1]
            f3 = features[2]
            if f1 == F1_NOUN and \
                    f2 != F2_IND_VERB and f2 != F2_NO_MEANING_NAMES and \
                    f2 != F2_ADVERBS and \
                    f2 != F2_PRONOUN and f2 != F2_ADJECTIVE and \
                    f2 != F2_NUMBER and \
                    f2 != F2_SUFFIX and \
                    f3 != F3_ADVERBS and \
                    node.surface not in STOPLIST:
                entity.append(node.surface.lower())
            else:
                if len(entity) > 0:
                    output.append(''.join(entity))
                    entity = []
            if f1 == F1_SEPARATOR and \
                    (f2 == '句点'):
                sentence += 1
            # move to next morphem
            node = node.next
        if (len(entity) > 0):
            output.append(entity)
        return output

    def extract_dates(self, content, with_year=None):
        """
        Extract dates from text in Japanese.
        """
        if with_year is None:
            with_year = str(datetime.now().year)
        # TODO: use regex module instead of re
        re_set = (
            re.compile(ur'\d{1,4}年\d{1,2}月\d{1,2}日', re.UNICODE),
            re.compile(ur'\d{1,2}月\d{1,2}日', re.UNICODE),
            # TODO: deal with days in text
            re.compile(ur'\d{1,4}/\d{1}/\d{1}', re.UNICODE),
            re.compile(ur'\d{1,2}/\d{1,2}', re.UNICODE)
        )
        res = []
        for re_i in re_set:
            res_i = re_i.findall(content.decode('utf8'))
            for el in res_i:
                parsed_date = parse(el)
                if parsed_date is not None:
                    formated_parsed_date = datetime.strftime(parsed_date,
                                                             '%Y-%m-%d')
                    if formated_parsed_date not in res:
                        res.append(formated_parsed_date)
        return res
