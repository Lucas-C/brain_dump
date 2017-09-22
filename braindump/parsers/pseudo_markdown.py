#!/usr/bin/python3

from pyparsing import CharsNotIn, Empty, Forward, Keyword, Literal, OneOrMore, Optional, QuotedString, Suppress, Token, White, Word, ZeroOrMore, delimitedList, nums, printables, ParseException


class StopOnSuffix(Token): # inspired by CharsNotIn
    def __init__(self, suffixes):
        super().__init__()
        self.skipWhitespace = False
        self.suffixes = set(suffixes)
        self.name = self.__class__.__name__
        self.mayReturnEmpty = True
        self.mayIndexError = False

    def parseImpl(self, instring, loc, doActions=True):
        if self._suffix_match(instring, loc):
            raise ParseException(instring, loc, '{} early stop : token starts with suffix'.format(self.name), self)
        start = loc
        maxlen = len(instring)
        loc += 1
        while loc < maxlen and not self._suffix_match(instring, loc):
            loc += 1
        return loc, instring[start:loc]

    def _suffix_match(self, instring, loc):
        for suffix in self.suffixes:
            suffix_length = len(suffix)
            if suffix == instring[loc:loc+suffix_length]:
                return True

Bold = Suppress(Literal('**'))
Italic = Suppress(Literal('__'))
Striked = Suppress(Literal('~~'))
Text = OneOrMore(Word(printables))

StyledText = Forward()
BoldText = (Bold + StyledText + Bold)('is_bold')
ItalicText = (Italic + StyledText + Italic)('is_italic')
StrikedText = (Striked + StyledText + Striked)('is_striked')
StyledText << (BoldText | ItalicText | StrikedText | StopOnSuffix(['**', '__', '~~', '!icon=', '<!--', '(see:']))
StyledText.resultsName = 'text'
StyledText.saveAsList = True  # must be done at this point, not before
TextGrammar = StyledText | Text.setResultsName('text', listAllMatches=True)

Checkbox = (Literal('[') + (Literal('x')('is_checked') | White()) + Literal(']'))('has_checkbox')

Icon = Literal('!icon=') + Word(printables).setResultsName('icons', listAllMatches=True)

DestNodeText = QuotedString('"', escChar='\\')
See = Keyword('(see:') + delimitedList(DestNodeText, delim=',').setResultsName('see') + Literal(')')

XMLAttrs = Literal('<!--') + StopOnSuffix(['-->']).setResultsName('attrs') + Literal('-->')

Url = CharsNotIn(') ')('url')
ImgDimensions = Word(nums)('img_width') + Literal('x') + Word(nums)('img_height')
Link = Optional(Literal('!'))('is_img') + Literal('[') + Optional(StopOnSuffix(['](']).setResultsName('text', listAllMatches=True)) + Literal('](') + Url + Optional(ImgDimensions) + Literal(')')

LineGrammar = Optional(Checkbox) + ZeroOrMore(Icon | XMLAttrs) + (Link | TextGrammar) + ZeroOrMore(Icon | XMLAttrs) + Optional(See)
