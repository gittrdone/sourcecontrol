# Generated from java-escape by ANTLR 4.4
from __future__ import print_function
from antlr4 import *
from io import StringIO
def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3")
        buf.write(u"\31e\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write(u"\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4")
        buf.write(u"\16\t\16\4\17\t\17\3\2\3\2\3\2\5\2\"\n\2\3\3\3\3\3\3")
        buf.write(u"\3\4\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\5\5\60\n\5\3\5\3")
        buf.write(u"\5\3\6\3\6\3\6\5\6\67\n\6\3\7\3\7\3\b\3\b\3\b\3\b\3\t")
        buf.write(u"\3\t\3\t\7\tB\n\t\f\t\16\tE\13\t\3\n\3\n\3\n\7\nJ\n\n")
        buf.write(u"\f\n\16\nM\13\n\3\13\3\13\3\13\5\13R\n\13\3\f\3\f\3\r")
        buf.write(u"\3\r\3\16\3\16\3\16\3\16\7\16\\\n\16\f\16\16\16_\13\16")
        buf.write(u"\3\16\3\16\3\17\3\17\3\17\2\2\20\2\4\6\b\n\f\16\20\22")
        buf.write(u"\24\26\30\32\34\2\4\5\2\5\6\17\17\21\21\7\2\b\b\13\r")
        buf.write(u"\20\20\23\23\25\25_\2!\3\2\2\2\4#\3\2\2\2\6&\3\2\2\2")
        buf.write(u"\b+\3\2\2\2\n\63\3\2\2\2\f8\3\2\2\2\16:\3\2\2\2\20>\3")
        buf.write(u"\2\2\2\22F\3\2\2\2\24Q\3\2\2\2\26S\3\2\2\2\30U\3\2\2")
        buf.write(u"\2\32W\3\2\2\2\34b\3\2\2\2\36\"\5\4\3\2\37\"\5\6\4\2")
        buf.write(u" \"\5\b\5\2!\36\3\2\2\2!\37\3\2\2\2! \3\2\2\2\"\3\3\2")
        buf.write(u"\2\2#$\7\16\2\2$%\5\n\6\2%\5\3\2\2\2&\'\7\7\2\2\'(\5")
        buf.write(u"\22\n\2()\7\3\2\2)*\5\n\6\2*\7\3\2\2\2+/\7\24\2\2,-\5")
        buf.write(u"\22\n\2-.\7\3\2\2.\60\3\2\2\2/,\3\2\2\2/\60\3\2\2\2\60")
        buf.write(u"\61\3\2\2\2\61\62\5\n\6\2\62\t\3\2\2\2\63\66\5\f\7\2")
        buf.write(u"\64\65\7\22\2\2\65\67\5\20\t\2\66\64\3\2\2\2\66\67\3")
        buf.write(u"\2\2\2\67\13\3\2\2\289\t\2\2\29\r\3\2\2\2:;\5\26\f\2")
        buf.write(u";<\5\34\17\2<=\5\24\13\2=\17\3\2\2\2>C\5\16\b\2?@\7\t")
        buf.write(u"\2\2@B\5\16\b\2A?\3\2\2\2BE\3\2\2\2CA\3\2\2\2CD\3\2\2")
        buf.write(u"\2D\21\3\2\2\2EC\3\2\2\2FK\5\26\f\2GH\7\t\2\2HJ\5\26")
        buf.write(u"\f\2IG\3\2\2\2JM\3\2\2\2KI\3\2\2\2KL\3\2\2\2L\23\3\2")
        buf.write(u"\2\2MK\3\2\2\2NR\7\26\2\2OR\7\27\2\2PR\5\32\16\2QN\3")
        buf.write(u"\2\2\2QO\3\2\2\2QP\3\2\2\2R\25\3\2\2\2ST\7\30\2\2T\27")
        buf.write(u"\3\2\2\2UV\7\27\2\2V\31\3\2\2\2WX\7\n\2\2X]\5\24\13\2")
        buf.write(u"YZ\7\t\2\2Z\\\5\24\13\2[Y\3\2\2\2\\_\3\2\2\2][\3\2\2")
        buf.write(u"\2]^\3\2\2\2^`\3\2\2\2_]\3\2\2\2`a\7\4\2\2a\33\3\2\2")
        buf.write(u"\2bc\t\3\2\2c\35\3\2\2\2\t!/\66CKQ]")
        return buf.getvalue()
		

class SourceControlParser ( Parser ):

    grammarFileName = "java-escape"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    EOF = Token.EOF
    T__18=1
    T__17=2
    T__16=3
    T__15=4
    T__14=5
    T__13=6
    T__12=7
    T__11=8
    T__10=9
    T__9=10
    T__8=11
    T__7=12
    T__6=13
    T__5=14
    T__4=15
    T__3=16
    T__2=17
    T__1=18
    T__0=19
    INT=20
    STRING=21
    ATTR_NAME=22
    WS=23

    tokenNames = [ u"<INVALID>", u"'from'", u"']'", u"'files'", u"'users'", 
                   u"'get'", u"'in'", u"','", u"'['", u"'<'", u"'='", u"'!='", 
                   u"'find'", u"'commits'", u"'>'", u"'branches'", u"'where'", 
                   u"'not in'", u"'count'", u"'contains'", u"INT", u"STRING", 
                   u"ATTR_NAME", u"WS" ]

    RULE_command = 0
    RULE_find = 1
    RULE_get = 2
    RULE_count = 3
    RULE_query = 4
    RULE_dataType = 5
    RULE_cond = 6
    RULE_condList = 7
    RULE_getList = 8
    RULE_value = 9
    RULE_attrName = 10
    RULE_valueName = 11
    RULE_vlist = 12
    RULE_comparator = 13

    ruleNames =  [ u"command", u"find", u"get", u"count", u"query", u"dataType", 
                   u"cond", u"condList", u"getList", u"value", u"attrName", 
                   u"valueName", u"vlist", u"comparator" ]

    def __init__(self, input):
        super(SourceControlParser, self).__init__(input)
        self.checkVersion("4.4")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class CommandContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SourceControlParser.CommandContext, self).__init__(parent, invokingState)
            self.parser = parser

        def find(self):
            return self.getTypedRuleContext(SourceControlParser.FindContext,0)


        def count(self):
            return self.getTypedRuleContext(SourceControlParser.CountContext,0)


        def get(self):
            return self.getTypedRuleContext(SourceControlParser.GetContext,0)


        def getRuleIndex(self):
            return SourceControlParser.RULE_command




    def command(self):

        localctx = SourceControlParser.CommandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_command)
        try:
            self.state = 31
            token = self._input.LA(1)
            if token in [self.T__7]:
                self.enterOuterAlt(localctx, 1)
                self.state = 28 
                self.find()

            elif token in [self.T__14]:
                self.enterOuterAlt(localctx, 2)
                self.state = 29 
                self.get()

            elif token in [self.T__1]:
                self.enterOuterAlt(localctx, 3)
                self.state = 30 
                self.count()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FindContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SourceControlParser.FindContext, self).__init__(parent, invokingState)
            self.parser = parser

        def query(self):
            return self.getTypedRuleContext(SourceControlParser.QueryContext,0)


        def getRuleIndex(self):
            return SourceControlParser.RULE_find




    def find(self):

        localctx = SourceControlParser.FindContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_find)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 33
            self.match(self.T__7)
            self.state = 34 
            self.query()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class GetContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SourceControlParser.GetContext, self).__init__(parent, invokingState)
            self.parser = parser

        def query(self):
            return self.getTypedRuleContext(SourceControlParser.QueryContext,0)


        def getList(self):
            return self.getTypedRuleContext(SourceControlParser.GetListContext,0)


        def getRuleIndex(self):
            return SourceControlParser.RULE_get




    def get(self):

        localctx = SourceControlParser.GetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_get)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.match(self.T__14)
            self.state = 37 
            self.getList()
            self.state = 38
            self.match(self.T__18)
            self.state = 39 
            self.query()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CountContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SourceControlParser.CountContext, self).__init__(parent, invokingState)
            self.parser = parser

        def query(self):
            return self.getTypedRuleContext(SourceControlParser.QueryContext,0)


        def getList(self):
            return self.getTypedRuleContext(SourceControlParser.GetListContext,0)


        def getRuleIndex(self):
            return SourceControlParser.RULE_count




    def count(self):

        localctx = SourceControlParser.CountContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_count)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41
            self.match(self.T__1)
            self.state = 45
            _la = self._input.LA(1)
            if _la==SourceControlParser.ATTR_NAME:
                self.state = 42 
                self.getList()
                self.state = 43
                self.match(self.T__18)


            self.state = 47 
            self.query()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class QueryContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SourceControlParser.QueryContext, self).__init__(parent, invokingState)
            self.parser = parser

        def condList(self):
            return self.getTypedRuleContext(SourceControlParser.CondListContext,0)


        def dataType(self):
            return self.getTypedRuleContext(SourceControlParser.DataTypeContext,0)


        def getRuleIndex(self):
            return SourceControlParser.RULE_query




    def query(self):

        localctx = SourceControlParser.QueryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_query)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 49 
            self.dataType()
            self.state = 52
            _la = self._input.LA(1)
            if _la==SourceControlParser.T__3:
                self.state = 50
                self.match(self.T__3)
                self.state = 51 
                self.condList()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DataTypeContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SourceControlParser.DataTypeContext, self).__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return SourceControlParser.RULE_dataType




    def dataType(self):

        localctx = SourceControlParser.DataTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_dataType)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 54
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << self.T__16) | (1 << self.T__15) | (1 << self.T__6) | (1 << self.T__4))) != 0)):
                self._errHandler.recoverInline(self)
            self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CondContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SourceControlParser.CondContext, self).__init__(parent, invokingState)
            self.parser = parser

        def attrName(self):
            return self.getTypedRuleContext(SourceControlParser.AttrNameContext,0)


        def value(self):
            return self.getTypedRuleContext(SourceControlParser.ValueContext,0)


        def comparator(self):
            return self.getTypedRuleContext(SourceControlParser.ComparatorContext,0)


        def getRuleIndex(self):
            return SourceControlParser.RULE_cond




    def cond(self):

        localctx = SourceControlParser.CondContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_cond)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 56 
            self.attrName()
            self.state = 57 
            self.comparator()
            self.state = 58 
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CondListContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SourceControlParser.CondListContext, self).__init__(parent, invokingState)
            self.parser = parser

        def cond(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SourceControlParser.CondContext)
            else:
                return self.getTypedRuleContext(SourceControlParser.CondContext,i)


        def getRuleIndex(self):
            return SourceControlParser.RULE_condList




    def condList(self):

        localctx = SourceControlParser.CondListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_condList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60 
            self.cond()
            self.state = 65
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SourceControlParser.T__12:
                self.state = 61
                self.match(self.T__12)
                self.state = 62 
                self.cond()
                self.state = 67
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class GetListContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SourceControlParser.GetListContext, self).__init__(parent, invokingState)
            self.parser = parser

        def attrName(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SourceControlParser.AttrNameContext)
            else:
                return self.getTypedRuleContext(SourceControlParser.AttrNameContext,i)


        def getRuleIndex(self):
            return SourceControlParser.RULE_getList




    def getList(self):

        localctx = SourceControlParser.GetListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_getList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 68 
            self.attrName()
            self.state = 73
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SourceControlParser.T__12:
                self.state = 69
                self.match(self.T__12)
                self.state = 70 
                self.attrName()
                self.state = 75
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ValueContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SourceControlParser.ValueContext, self).__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(SourceControlParser.INT, 0)

        def vlist(self):
            return self.getTypedRuleContext(SourceControlParser.VlistContext,0)


        def STRING(self):
            return self.getToken(SourceControlParser.STRING, 0)

        def getRuleIndex(self):
            return SourceControlParser.RULE_value




    def value(self):

        localctx = SourceControlParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_value)
        try:
            self.state = 79
            token = self._input.LA(1)
            if token in [self.INT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 76
                self.match(self.INT)

            elif token in [self.STRING]:
                self.enterOuterAlt(localctx, 2)
                self.state = 77
                self.match(self.STRING)

            elif token in [self.T__11]:
                self.enterOuterAlt(localctx, 3)
                self.state = 78 
                self.vlist()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AttrNameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SourceControlParser.AttrNameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ATTR_NAME(self):
            return self.getToken(SourceControlParser.ATTR_NAME, 0)

        def getRuleIndex(self):
            return SourceControlParser.RULE_attrName




    def attrName(self):

        localctx = SourceControlParser.AttrNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_attrName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 81
            self.match(self.ATTR_NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ValueNameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SourceControlParser.ValueNameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(SourceControlParser.STRING, 0)

        def getRuleIndex(self):
            return SourceControlParser.RULE_valueName




    def valueName(self):

        localctx = SourceControlParser.ValueNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_valueName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            self.match(self.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class VlistContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SourceControlParser.VlistContext, self).__init__(parent, invokingState)
            self.parser = parser

        def value(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SourceControlParser.ValueContext)
            else:
                return self.getTypedRuleContext(SourceControlParser.ValueContext,i)


        def getRuleIndex(self):
            return SourceControlParser.RULE_vlist




    def vlist(self):

        localctx = SourceControlParser.VlistContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_vlist)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            self.match(self.T__11)
            self.state = 86 
            self.value()
            self.state = 91
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SourceControlParser.T__12:
                self.state = 87
                self.match(self.T__12)
                self.state = 88 
                self.value()
                self.state = 93
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 94
            self.match(self.T__17)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ComparatorContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SourceControlParser.ComparatorContext, self).__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return SourceControlParser.RULE_comparator




    def comparator(self):

        localctx = SourceControlParser.ComparatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_comparator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 96
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << self.T__13) | (1 << self.T__10) | (1 << self.T__9) | (1 << self.T__8) | (1 << self.T__5) | (1 << self.T__2) | (1 << self.T__0))) != 0)):
                self._errHandler.recoverInline(self)
            self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx




