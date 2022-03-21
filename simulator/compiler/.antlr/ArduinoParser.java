// Generated from e:\Asignaturas\Cuarto\TFG\SimuladorSoftwareRobots\simulator\compiler\Arduino.g4 by ANTLR 4.8
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class ArduinoParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.8", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, T__15=16, T__16=17, 
		T__17=18, T__18=19, T__19=20, T__20=21, T__21=22, T__22=23, T__23=24, 
		T__24=25, T__25=26, T__26=27, T__27=28, T__28=29, T__29=30, T__30=31, 
		T__31=32, T__32=33, T__33=34, T__34=35, T__35=36, T__36=37, T__37=38, 
		T__38=39, T__39=40, T__40=41, T__41=42, T__42=43, T__43=44, T__44=45, 
		T__45=46, T__46=47, T__47=48, T__48=49, T__49=50, T__50=51, T__51=52, 
		T__52=53, T__53=54, T__54=55, T__55=56, T__56=57, T__57=58, T__58=59, 
		T__59=60, T__60=61, T__61=62, T__62=63, T__63=64, T__64=65, T__65=66, 
		T__66=67, T__67=68, T__68=69, T__69=70, T__70=71, T__71=72, BIT_SHIFT_L=73, 
		BIT_SHIFT_R=74, BINARY_CONST=75, OCTAL_CONST=76, HEX_CONST=77, INT_CONST=78, 
		FLOAT_CONST=79, CHAR_CONST=80, UNTERMINATED_CHAR=81, STRING_CONST=82, 
		UNTERMINATED_STRING=83, ID=84, LINE_COMMENT=85, MULTILINE_COMMENT=86, 
		WHITESPACE=87;
	public static final int
		RULE_start = 0, RULE_program = 1, RULE_include = 2, RULE_program_code = 3, 
		RULE_declaration = 4, RULE_simple_declaration = 5, RULE_array_declaration = 6, 
		RULE_define_macro = 7, RULE_array_index = 8, RULE_array_elements = 9, 
		RULE_var_type = 10, RULE_function = 11, RULE_function_args = 12, RULE_iteration_sentence = 13, 
		RULE_conditional_sentence = 14, RULE_code_block = 15, RULE_sentence = 16, 
		RULE_assignment = 17, RULE_case_sentence = 18, RULE_expression = 19, RULE_function_call = 20, 
		RULE_parameter = 21;
	private static String[] makeRuleNames() {
		return new String[] {
			"start", "program", "include", "program_code", "declaration", "simple_declaration", 
			"array_declaration", "define_macro", "array_index", "array_elements", 
			"var_type", "function", "function_args", "iteration_sentence", "conditional_sentence", 
			"code_block", "sentence", "assignment", "case_sentence", "expression", 
			"function_call", "parameter"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'#include'", "'<'", "'.'", "'>'", "';'", "'const'", "'static'", 
			"'='", "'#define'", "'['", "']'", "'{'", "','", "'}'", "'bool'", "'boolean'", 
			"'byte'", "'char'", "'double'", "'float'", "'int'", "'long'", "'short'", 
			"'size_t'", "'String'", "'unsigned int'", "'unsigned char'", "'unsigned long'", 
			"'void'", "'word'", "'('", "')'", "'while'", "'do'", "'for'", "'if'", 
			"'else'", "'switch'", "'return'", "'break'", "'continue'", "'case'", 
			"':'", "'default'", "'true'", "'false'", "'++'", "'--'", "'!'", "'~'", 
			"'*'", "'/'", "'%'", "'+'", "'-'", "'>='", "'<='", "'=='", "'!='", "'&'", 
			"'^'", "'|'", "'&&'", "'||'", "'%='", "'&='", "'*='", "'+='", "'-='", 
			"'/='", "'^='", "'|='"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, "BIT_SHIFT_L", "BIT_SHIFT_R", "BINARY_CONST", "OCTAL_CONST", "HEX_CONST", 
			"INT_CONST", "FLOAT_CONST", "CHAR_CONST", "UNTERMINATED_CHAR", "STRING_CONST", 
			"UNTERMINATED_STRING", "ID", "LINE_COMMENT", "MULTILINE_COMMENT", "WHITESPACE"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "Arduino.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public ArduinoParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	public static class StartContext extends ParserRuleContext {
		public ProgramContext program() {
			return getRuleContext(ProgramContext.class,0);
		}
		public TerminalNode EOF() { return getToken(ArduinoParser.EOF, 0); }
		public StartContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_start; }
	}

	public final StartContext start() throws RecognitionException {
		StartContext _localctx = new StartContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_start);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(44);
			program();
			setState(45);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ProgramContext extends ParserRuleContext {
		public IncludeContext include;
		public List<IncludeContext> include_directives = new ArrayList<IncludeContext>();
		public Program_codeContext program_code;
		public List<Program_codeContext> code = new ArrayList<Program_codeContext>();
		public List<IncludeContext> include() {
			return getRuleContexts(IncludeContext.class);
		}
		public IncludeContext include(int i) {
			return getRuleContext(IncludeContext.class,i);
		}
		public List<Program_codeContext> program_code() {
			return getRuleContexts(Program_codeContext.class);
		}
		public Program_codeContext program_code(int i) {
			return getRuleContext(Program_codeContext.class,i);
		}
		public ProgramContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_program; }
	}

	public final ProgramContext program() throws RecognitionException {
		ProgramContext _localctx = new ProgramContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_program);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(50);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__0) {
				{
				{
				setState(47);
				((ProgramContext)_localctx).include = include();
				((ProgramContext)_localctx).include_directives.add(((ProgramContext)_localctx).include);
				}
				}
				setState(52);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(56);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__5) | (1L << T__6) | (1L << T__8) | (1L << T__14) | (1L << T__15) | (1L << T__16) | (1L << T__17) | (1L << T__18) | (1L << T__19) | (1L << T__20) | (1L << T__21) | (1L << T__22) | (1L << T__23) | (1L << T__24) | (1L << T__25) | (1L << T__26) | (1L << T__27) | (1L << T__28) | (1L << T__29))) != 0) || _la==ID) {
				{
				{
				setState(53);
				((ProgramContext)_localctx).program_code = program_code();
				((ProgramContext)_localctx).code.add(((ProgramContext)_localctx).program_code);
				}
				}
				setState(58);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class IncludeContext extends ParserRuleContext {
		public TerminalNode STRING_CONST() { return getToken(ArduinoParser.STRING_CONST, 0); }
		public List<TerminalNode> ID() { return getTokens(ArduinoParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(ArduinoParser.ID, i);
		}
		public IncludeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_include; }
	}

	public final IncludeContext include() throws RecognitionException {
		IncludeContext _localctx = new IncludeContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_include);
		try {
			setState(67);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,2,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(59);
				match(T__0);
				setState(60);
				match(STRING_CONST);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(61);
				match(T__0);
				setState(62);
				match(T__1);
				setState(63);
				match(ID);
				setState(64);
				match(T__2);
				setState(65);
				match(ID);
				setState(66);
				match(T__3);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Program_codeContext extends ParserRuleContext {
		public DeclarationContext var_dec;
		public FunctionContext func_def;
		public Define_macroContext def_mac;
		public DeclarationContext declaration() {
			return getRuleContext(DeclarationContext.class,0);
		}
		public FunctionContext function() {
			return getRuleContext(FunctionContext.class,0);
		}
		public Define_macroContext define_macro() {
			return getRuleContext(Define_macroContext.class,0);
		}
		public Program_codeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_program_code; }
	}

	public final Program_codeContext program_code() throws RecognitionException {
		Program_codeContext _localctx = new Program_codeContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_program_code);
		try {
			setState(74);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,3,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(69);
				((Program_codeContext)_localctx).var_dec = declaration();
				setState(70);
				match(T__4);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(72);
				((Program_codeContext)_localctx).func_def = function();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(73);
				((Program_codeContext)_localctx).def_mac = define_macro();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class DeclarationContext extends ParserRuleContext {
		public Simple_declarationContext s_def;
		public Array_declarationContext a_def;
		public Token qual;
		public Simple_declarationContext simple_declaration() {
			return getRuleContext(Simple_declarationContext.class,0);
		}
		public Array_declarationContext array_declaration() {
			return getRuleContext(Array_declarationContext.class,0);
		}
		public DeclarationContext declaration() {
			return getRuleContext(DeclarationContext.class,0);
		}
		public DeclarationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_declaration; }
	}

	public final DeclarationContext declaration() throws RecognitionException {
		DeclarationContext _localctx = new DeclarationContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_declaration);
		int _la;
		try {
			setState(80);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,4,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(76);
				((DeclarationContext)_localctx).s_def = simple_declaration();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(77);
				((DeclarationContext)_localctx).a_def = array_declaration();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(78);
				((DeclarationContext)_localctx).qual = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==T__5 || _la==T__6) ) {
					((DeclarationContext)_localctx).qual = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(79);
				declaration();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Simple_declarationContext extends ParserRuleContext {
		public Var_typeContext v_type;
		public ExpressionContext val;
		public TerminalNode ID() { return getToken(ArduinoParser.ID, 0); }
		public Var_typeContext var_type() {
			return getRuleContext(Var_typeContext.class,0);
		}
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public Simple_declarationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_simple_declaration; }
	}

	public final Simple_declarationContext simple_declaration() throws RecognitionException {
		Simple_declarationContext _localctx = new Simple_declarationContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_simple_declaration);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(82);
			((Simple_declarationContext)_localctx).v_type = var_type();
			setState(83);
			match(ID);
			setState(86);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__7) {
				{
				setState(84);
				match(T__7);
				setState(85);
				((Simple_declarationContext)_localctx).val = expression(0);
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Array_declarationContext extends ParserRuleContext {
		public Var_typeContext v_type;
		public Array_indexContext a_index;
		public ExpressionContext expr;
		public Array_elementsContext elems;
		public TerminalNode ID() { return getToken(ArduinoParser.ID, 0); }
		public Var_typeContext var_type() {
			return getRuleContext(Var_typeContext.class,0);
		}
		public Array_indexContext array_index() {
			return getRuleContext(Array_indexContext.class,0);
		}
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public Array_elementsContext array_elements() {
			return getRuleContext(Array_elementsContext.class,0);
		}
		public Array_declarationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_array_declaration; }
	}

	public final Array_declarationContext array_declaration() throws RecognitionException {
		Array_declarationContext _localctx = new Array_declarationContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_array_declaration);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(88);
			((Array_declarationContext)_localctx).v_type = var_type();
			setState(89);
			match(ID);
			setState(90);
			((Array_declarationContext)_localctx).a_index = array_index();
			setState(96);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__7) {
				{
				setState(91);
				match(T__7);
				setState(94);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case T__30:
				case T__44:
				case T__45:
				case T__46:
				case T__47:
				case T__48:
				case T__49:
				case BINARY_CONST:
				case OCTAL_CONST:
				case HEX_CONST:
				case INT_CONST:
				case FLOAT_CONST:
				case CHAR_CONST:
				case STRING_CONST:
				case ID:
					{
					setState(92);
					((Array_declarationContext)_localctx).expr = expression(0);
					}
					break;
				case T__11:
					{
					setState(93);
					((Array_declarationContext)_localctx).elems = array_elements();
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Define_macroContext extends ParserRuleContext {
		public ExpressionContext val;
		public Array_elementsContext elems;
		public TerminalNode ID() { return getToken(ArduinoParser.ID, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public Array_elementsContext array_elements() {
			return getRuleContext(Array_elementsContext.class,0);
		}
		public Define_macroContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_define_macro; }
	}

	public final Define_macroContext define_macro() throws RecognitionException {
		Define_macroContext _localctx = new Define_macroContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_define_macro);
		try {
			setState(104);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,8,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(98);
				match(T__8);
				setState(99);
				match(ID);
				setState(100);
				((Define_macroContext)_localctx).val = expression(0);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(101);
				match(T__8);
				setState(102);
				match(ID);
				setState(103);
				((Define_macroContext)_localctx).elems = array_elements();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Array_indexContext extends ParserRuleContext {
		public Token s10;
		public List<Token> dimensions = new ArrayList<Token>();
		public Token INT_CONST;
		public List<Token> sizes = new ArrayList<Token>();
		public List<TerminalNode> INT_CONST() { return getTokens(ArduinoParser.INT_CONST); }
		public TerminalNode INT_CONST(int i) {
			return getToken(ArduinoParser.INT_CONST, i);
		}
		public Array_indexContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_array_index; }
	}

	public final Array_indexContext array_index() throws RecognitionException {
		Array_indexContext _localctx = new Array_indexContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_array_index);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(106);
			((Array_indexContext)_localctx).s10 = match(T__9);
			((Array_indexContext)_localctx).dimensions.add(((Array_indexContext)_localctx).s10);
			setState(108);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==INT_CONST) {
				{
				setState(107);
				((Array_indexContext)_localctx).INT_CONST = match(INT_CONST);
				((Array_indexContext)_localctx).sizes.add(((Array_indexContext)_localctx).INT_CONST);
				}
			}

			setState(110);
			match(T__10);
			setState(116);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__9) {
				{
				{
				setState(111);
				((Array_indexContext)_localctx).s10 = match(T__9);
				((Array_indexContext)_localctx).dimensions.add(((Array_indexContext)_localctx).s10);
				setState(112);
				((Array_indexContext)_localctx).INT_CONST = match(INT_CONST);
				((Array_indexContext)_localctx).sizes.add(((Array_indexContext)_localctx).INT_CONST);
				setState(113);
				match(T__10);
				}
				}
				setState(118);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Array_elementsContext extends ParserRuleContext {
		public ExpressionContext expression;
		public List<ExpressionContext> elements = new ArrayList<ExpressionContext>();
		public List<Array_elementsContext> array_elements() {
			return getRuleContexts(Array_elementsContext.class);
		}
		public Array_elementsContext array_elements(int i) {
			return getRuleContext(Array_elementsContext.class,i);
		}
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public Array_elementsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_array_elements; }
	}

	public final Array_elementsContext array_elements() throws RecognitionException {
		Array_elementsContext _localctx = new Array_elementsContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_array_elements);
		int _la;
		try {
			setState(140);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,13,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(119);
				match(T__11);
				setState(120);
				array_elements();
				setState(123); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(121);
					match(T__12);
					setState(122);
					array_elements();
					}
					}
					setState(125); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==T__12 );
				setState(127);
				match(T__13);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(129);
				match(T__11);
				setState(130);
				((Array_elementsContext)_localctx).expression = expression(0);
				((Array_elementsContext)_localctx).elements.add(((Array_elementsContext)_localctx).expression);
				setState(135);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__12) {
					{
					{
					setState(131);
					match(T__12);
					setState(132);
					((Array_elementsContext)_localctx).expression = expression(0);
					((Array_elementsContext)_localctx).elements.add(((Array_elementsContext)_localctx).expression);
					}
					}
					setState(137);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(138);
				match(T__13);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Var_typeContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(ArduinoParser.ID, 0); }
		public Var_typeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_var_type; }
	}

	public final Var_typeContext var_type() throws RecognitionException {
		Var_typeContext _localctx = new Var_typeContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_var_type);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(142);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__14) | (1L << T__15) | (1L << T__16) | (1L << T__17) | (1L << T__18) | (1L << T__19) | (1L << T__20) | (1L << T__21) | (1L << T__22) | (1L << T__23) | (1L << T__24) | (1L << T__25) | (1L << T__26) | (1L << T__27) | (1L << T__28) | (1L << T__29))) != 0) || _la==ID) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class FunctionContext extends ParserRuleContext {
		public Var_typeContext v_type;
		public Function_argsContext f_args;
		public SentenceContext sentence;
		public List<SentenceContext> sentences = new ArrayList<SentenceContext>();
		public TerminalNode ID() { return getToken(ArduinoParser.ID, 0); }
		public Var_typeContext var_type() {
			return getRuleContext(Var_typeContext.class,0);
		}
		public Function_argsContext function_args() {
			return getRuleContext(Function_argsContext.class,0);
		}
		public List<SentenceContext> sentence() {
			return getRuleContexts(SentenceContext.class);
		}
		public SentenceContext sentence(int i) {
			return getRuleContext(SentenceContext.class,i);
		}
		public FunctionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_function; }
	}

	public final FunctionContext function() throws RecognitionException {
		FunctionContext _localctx = new FunctionContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_function);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(144);
			((FunctionContext)_localctx).v_type = var_type();
			setState(145);
			match(ID);
			setState(146);
			match(T__30);
			setState(148);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__5) | (1L << T__6) | (1L << T__14) | (1L << T__15) | (1L << T__16) | (1L << T__17) | (1L << T__18) | (1L << T__19) | (1L << T__20) | (1L << T__21) | (1L << T__22) | (1L << T__23) | (1L << T__24) | (1L << T__25) | (1L << T__26) | (1L << T__27) | (1L << T__28) | (1L << T__29))) != 0) || _la==ID) {
				{
				setState(147);
				((FunctionContext)_localctx).f_args = function_args();
				}
			}

			setState(150);
			match(T__31);
			setState(151);
			match(T__11);
			setState(155);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__5) | (1L << T__6) | (1L << T__8) | (1L << T__14) | (1L << T__15) | (1L << T__16) | (1L << T__17) | (1L << T__18) | (1L << T__19) | (1L << T__20) | (1L << T__21) | (1L << T__22) | (1L << T__23) | (1L << T__24) | (1L << T__25) | (1L << T__26) | (1L << T__27) | (1L << T__28) | (1L << T__29) | (1L << T__30) | (1L << T__32) | (1L << T__33) | (1L << T__34) | (1L << T__35) | (1L << T__37) | (1L << T__38) | (1L << T__39) | (1L << T__40) | (1L << T__44) | (1L << T__45) | (1L << T__46) | (1L << T__47) | (1L << T__48) | (1L << T__49))) != 0) || ((((_la - 75)) & ~0x3f) == 0 && ((1L << (_la - 75)) & ((1L << (BINARY_CONST - 75)) | (1L << (OCTAL_CONST - 75)) | (1L << (HEX_CONST - 75)) | (1L << (INT_CONST - 75)) | (1L << (FLOAT_CONST - 75)) | (1L << (CHAR_CONST - 75)) | (1L << (STRING_CONST - 75)) | (1L << (ID - 75)))) != 0)) {
				{
				{
				setState(152);
				((FunctionContext)_localctx).sentence = sentence();
				((FunctionContext)_localctx).sentences.add(((FunctionContext)_localctx).sentence);
				}
				}
				setState(157);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(158);
			match(T__13);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Function_argsContext extends ParserRuleContext {
		public DeclarationContext declaration;
		public List<DeclarationContext> f_args = new ArrayList<DeclarationContext>();
		public List<DeclarationContext> declaration() {
			return getRuleContexts(DeclarationContext.class);
		}
		public DeclarationContext declaration(int i) {
			return getRuleContext(DeclarationContext.class,i);
		}
		public Function_argsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_function_args; }
	}

	public final Function_argsContext function_args() throws RecognitionException {
		Function_argsContext _localctx = new Function_argsContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_function_args);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(160);
			((Function_argsContext)_localctx).declaration = declaration();
			((Function_argsContext)_localctx).f_args.add(((Function_argsContext)_localctx).declaration);
			setState(165);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__12) {
				{
				{
				setState(161);
				match(T__12);
				setState(162);
				((Function_argsContext)_localctx).declaration = declaration();
				((Function_argsContext)_localctx).f_args.add(((Function_argsContext)_localctx).declaration);
				}
				}
				setState(167);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Iteration_sentenceContext extends ParserRuleContext {
		public Token it_type;
		public ExpressionContext expr;
		public Code_blockContext code;
		public Simple_declarationContext assign_def;
		public ExpressionContext condition;
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public Code_blockContext code_block() {
			return getRuleContext(Code_blockContext.class,0);
		}
		public Simple_declarationContext simple_declaration() {
			return getRuleContext(Simple_declarationContext.class,0);
		}
		public Iteration_sentenceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_iteration_sentence; }
	}

	public final Iteration_sentenceContext iteration_sentence() throws RecognitionException {
		Iteration_sentenceContext _localctx = new Iteration_sentenceContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_iteration_sentence);
		int _la;
		try {
			setState(197);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__32:
				enterOuterAlt(_localctx, 1);
				{
				setState(168);
				((Iteration_sentenceContext)_localctx).it_type = match(T__32);
				setState(169);
				match(T__30);
				setState(170);
				((Iteration_sentenceContext)_localctx).expr = expression(0);
				setState(171);
				match(T__31);
				setState(172);
				((Iteration_sentenceContext)_localctx).code = code_block();
				}
				break;
			case T__33:
				enterOuterAlt(_localctx, 2);
				{
				setState(174);
				((Iteration_sentenceContext)_localctx).it_type = match(T__33);
				setState(175);
				((Iteration_sentenceContext)_localctx).code = code_block();
				setState(176);
				match(T__32);
				setState(177);
				match(T__30);
				setState(178);
				((Iteration_sentenceContext)_localctx).expr = expression(0);
				setState(179);
				match(T__31);
				setState(180);
				match(T__4);
				}
				break;
			case T__34:
				enterOuterAlt(_localctx, 3);
				{
				setState(182);
				((Iteration_sentenceContext)_localctx).it_type = match(T__34);
				setState(183);
				match(T__30);
				setState(185);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__14) | (1L << T__15) | (1L << T__16) | (1L << T__17) | (1L << T__18) | (1L << T__19) | (1L << T__20) | (1L << T__21) | (1L << T__22) | (1L << T__23) | (1L << T__24) | (1L << T__25) | (1L << T__26) | (1L << T__27) | (1L << T__28) | (1L << T__29))) != 0) || _la==ID) {
					{
					setState(184);
					((Iteration_sentenceContext)_localctx).assign_def = simple_declaration();
					}
				}

				setState(187);
				match(T__4);
				setState(189);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (((((_la - 31)) & ~0x3f) == 0 && ((1L << (_la - 31)) & ((1L << (T__30 - 31)) | (1L << (T__44 - 31)) | (1L << (T__45 - 31)) | (1L << (T__46 - 31)) | (1L << (T__47 - 31)) | (1L << (T__48 - 31)) | (1L << (T__49 - 31)) | (1L << (BINARY_CONST - 31)) | (1L << (OCTAL_CONST - 31)) | (1L << (HEX_CONST - 31)) | (1L << (INT_CONST - 31)) | (1L << (FLOAT_CONST - 31)) | (1L << (CHAR_CONST - 31)) | (1L << (STRING_CONST - 31)) | (1L << (ID - 31)))) != 0)) {
					{
					setState(188);
					((Iteration_sentenceContext)_localctx).condition = expression(0);
					}
				}

				setState(191);
				match(T__4);
				setState(193);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (((((_la - 31)) & ~0x3f) == 0 && ((1L << (_la - 31)) & ((1L << (T__30 - 31)) | (1L << (T__44 - 31)) | (1L << (T__45 - 31)) | (1L << (T__46 - 31)) | (1L << (T__47 - 31)) | (1L << (T__48 - 31)) | (1L << (T__49 - 31)) | (1L << (BINARY_CONST - 31)) | (1L << (OCTAL_CONST - 31)) | (1L << (HEX_CONST - 31)) | (1L << (INT_CONST - 31)) | (1L << (FLOAT_CONST - 31)) | (1L << (CHAR_CONST - 31)) | (1L << (STRING_CONST - 31)) | (1L << (ID - 31)))) != 0)) {
					{
					setState(192);
					((Iteration_sentenceContext)_localctx).expr = expression(0);
					}
				}

				setState(195);
				match(T__31);
				setState(196);
				((Iteration_sentenceContext)_localctx).code = code_block();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Conditional_sentenceContext extends ParserRuleContext {
		public Token cond_type;
		public ExpressionContext expr;
		public Code_blockContext if_code;
		public Code_blockContext else_code;
		public Case_sentenceContext case_sentence;
		public List<Case_sentenceContext> sentences = new ArrayList<Case_sentenceContext>();
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public List<Code_blockContext> code_block() {
			return getRuleContexts(Code_blockContext.class);
		}
		public Code_blockContext code_block(int i) {
			return getRuleContext(Code_blockContext.class,i);
		}
		public List<Case_sentenceContext> case_sentence() {
			return getRuleContexts(Case_sentenceContext.class);
		}
		public Case_sentenceContext case_sentence(int i) {
			return getRuleContext(Case_sentenceContext.class,i);
		}
		public Conditional_sentenceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_conditional_sentence; }
	}

	public final Conditional_sentenceContext conditional_sentence() throws RecognitionException {
		Conditional_sentenceContext _localctx = new Conditional_sentenceContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_conditional_sentence);
		int _la;
		try {
			setState(221);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__35:
				enterOuterAlt(_localctx, 1);
				{
				setState(199);
				((Conditional_sentenceContext)_localctx).cond_type = match(T__35);
				setState(200);
				match(T__30);
				setState(201);
				((Conditional_sentenceContext)_localctx).expr = expression(0);
				setState(202);
				match(T__31);
				setState(203);
				((Conditional_sentenceContext)_localctx).if_code = code_block();
				setState(206);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,21,_ctx) ) {
				case 1:
					{
					setState(204);
					match(T__36);
					setState(205);
					((Conditional_sentenceContext)_localctx).else_code = code_block();
					}
					break;
				}
				}
				break;
			case T__37:
				enterOuterAlt(_localctx, 2);
				{
				setState(208);
				((Conditional_sentenceContext)_localctx).cond_type = match(T__37);
				setState(209);
				match(T__30);
				setState(210);
				((Conditional_sentenceContext)_localctx).expr = expression(0);
				setState(211);
				match(T__31);
				setState(212);
				match(T__11);
				setState(216);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__41 || _la==T__43) {
					{
					{
					setState(213);
					((Conditional_sentenceContext)_localctx).case_sentence = case_sentence();
					((Conditional_sentenceContext)_localctx).sentences.add(((Conditional_sentenceContext)_localctx).case_sentence);
					}
					}
					setState(218);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(219);
				match(T__13);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Code_blockContext extends ParserRuleContext {
		public SentenceContext sentence;
		public List<SentenceContext> sentences = new ArrayList<SentenceContext>();
		public List<SentenceContext> sentence() {
			return getRuleContexts(SentenceContext.class);
		}
		public SentenceContext sentence(int i) {
			return getRuleContext(SentenceContext.class,i);
		}
		public Code_blockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_code_block; }
	}

	public final Code_blockContext code_block() throws RecognitionException {
		Code_blockContext _localctx = new Code_blockContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_code_block);
		int _la;
		try {
			setState(232);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__11:
				enterOuterAlt(_localctx, 1);
				{
				setState(223);
				match(T__11);
				setState(227);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__5) | (1L << T__6) | (1L << T__8) | (1L << T__14) | (1L << T__15) | (1L << T__16) | (1L << T__17) | (1L << T__18) | (1L << T__19) | (1L << T__20) | (1L << T__21) | (1L << T__22) | (1L << T__23) | (1L << T__24) | (1L << T__25) | (1L << T__26) | (1L << T__27) | (1L << T__28) | (1L << T__29) | (1L << T__30) | (1L << T__32) | (1L << T__33) | (1L << T__34) | (1L << T__35) | (1L << T__37) | (1L << T__38) | (1L << T__39) | (1L << T__40) | (1L << T__44) | (1L << T__45) | (1L << T__46) | (1L << T__47) | (1L << T__48) | (1L << T__49))) != 0) || ((((_la - 75)) & ~0x3f) == 0 && ((1L << (_la - 75)) & ((1L << (BINARY_CONST - 75)) | (1L << (OCTAL_CONST - 75)) | (1L << (HEX_CONST - 75)) | (1L << (INT_CONST - 75)) | (1L << (FLOAT_CONST - 75)) | (1L << (CHAR_CONST - 75)) | (1L << (STRING_CONST - 75)) | (1L << (ID - 75)))) != 0)) {
					{
					{
					setState(224);
					((Code_blockContext)_localctx).sentence = sentence();
					((Code_blockContext)_localctx).sentences.add(((Code_blockContext)_localctx).sentence);
					}
					}
					setState(229);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(230);
				match(T__13);
				}
				break;
			case T__5:
			case T__6:
			case T__8:
			case T__14:
			case T__15:
			case T__16:
			case T__17:
			case T__18:
			case T__19:
			case T__20:
			case T__21:
			case T__22:
			case T__23:
			case T__24:
			case T__25:
			case T__26:
			case T__27:
			case T__28:
			case T__29:
			case T__30:
			case T__32:
			case T__33:
			case T__34:
			case T__35:
			case T__37:
			case T__38:
			case T__39:
			case T__40:
			case T__44:
			case T__45:
			case T__46:
			case T__47:
			case T__48:
			case T__49:
			case BINARY_CONST:
			case OCTAL_CONST:
			case HEX_CONST:
			case INT_CONST:
			case FLOAT_CONST:
			case CHAR_CONST:
			case STRING_CONST:
			case ID:
				enterOuterAlt(_localctx, 2);
				{
				setState(231);
				((Code_blockContext)_localctx).sentence = sentence();
				((Code_blockContext)_localctx).sentences.add(((Code_blockContext)_localctx).sentence);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class SentenceContext extends ParserRuleContext {
		public DeclarationContext dec;
		public Iteration_sentenceContext it_sent;
		public Conditional_sentenceContext cond_sent;
		public AssignmentContext assign;
		public ExpressionContext expr;
		public Define_macroContext def_mac;
		public Token s_type;
		public DeclarationContext declaration() {
			return getRuleContext(DeclarationContext.class,0);
		}
		public Iteration_sentenceContext iteration_sentence() {
			return getRuleContext(Iteration_sentenceContext.class,0);
		}
		public Conditional_sentenceContext conditional_sentence() {
			return getRuleContext(Conditional_sentenceContext.class,0);
		}
		public AssignmentContext assignment() {
			return getRuleContext(AssignmentContext.class,0);
		}
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public Define_macroContext define_macro() {
			return getRuleContext(Define_macroContext.class,0);
		}
		public SentenceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sentence; }
	}

	public final SentenceContext sentence() throws RecognitionException {
		SentenceContext _localctx = new SentenceContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_sentence);
		int _la;
		try {
			setState(255);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,27,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(234);
				((SentenceContext)_localctx).dec = declaration();
				setState(235);
				match(T__4);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(237);
				((SentenceContext)_localctx).it_sent = iteration_sentence();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(238);
				((SentenceContext)_localctx).cond_sent = conditional_sentence();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(239);
				((SentenceContext)_localctx).assign = assignment();
				setState(240);
				match(T__4);
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(242);
				((SentenceContext)_localctx).expr = expression(0);
				setState(243);
				match(T__4);
				}
				break;
			case 6:
				enterOuterAlt(_localctx, 6);
				{
				setState(245);
				((SentenceContext)_localctx).def_mac = define_macro();
				}
				break;
			case 7:
				enterOuterAlt(_localctx, 7);
				{
				setState(246);
				((SentenceContext)_localctx).s_type = match(T__38);
				setState(248);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (((((_la - 31)) & ~0x3f) == 0 && ((1L << (_la - 31)) & ((1L << (T__30 - 31)) | (1L << (T__44 - 31)) | (1L << (T__45 - 31)) | (1L << (T__46 - 31)) | (1L << (T__47 - 31)) | (1L << (T__48 - 31)) | (1L << (T__49 - 31)) | (1L << (BINARY_CONST - 31)) | (1L << (OCTAL_CONST - 31)) | (1L << (HEX_CONST - 31)) | (1L << (INT_CONST - 31)) | (1L << (FLOAT_CONST - 31)) | (1L << (CHAR_CONST - 31)) | (1L << (STRING_CONST - 31)) | (1L << (ID - 31)))) != 0)) {
					{
					setState(247);
					((SentenceContext)_localctx).expr = expression(0);
					}
				}

				setState(250);
				match(T__4);
				}
				break;
			case 8:
				enterOuterAlt(_localctx, 8);
				{
				setState(251);
				((SentenceContext)_localctx).s_type = match(T__39);
				setState(252);
				match(T__4);
				}
				break;
			case 9:
				enterOuterAlt(_localctx, 9);
				{
				setState(253);
				((SentenceContext)_localctx).s_type = match(T__40);
				setState(254);
				match(T__4);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class AssignmentContext extends ParserRuleContext {
		public ExpressionContext assign;
		public ExpressionContext value;
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public AssignmentContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_assignment; }
	}

	public final AssignmentContext assignment() throws RecognitionException {
		AssignmentContext _localctx = new AssignmentContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_assignment);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(257);
			((AssignmentContext)_localctx).assign = expression(0);
			setState(258);
			match(T__7);
			setState(259);
			((AssignmentContext)_localctx).value = expression(0);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Case_sentenceContext extends ParserRuleContext {
		public Token sent_type;
		public ExpressionContext expr;
		public SentenceContext sentence;
		public List<SentenceContext> sentences = new ArrayList<SentenceContext>();
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public List<SentenceContext> sentence() {
			return getRuleContexts(SentenceContext.class);
		}
		public SentenceContext sentence(int i) {
			return getRuleContext(SentenceContext.class,i);
		}
		public Case_sentenceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_case_sentence; }
	}

	public final Case_sentenceContext case_sentence() throws RecognitionException {
		Case_sentenceContext _localctx = new Case_sentenceContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_case_sentence);
		try {
			int _alt;
			setState(283);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__41:
				enterOuterAlt(_localctx, 1);
				{
				setState(261);
				((Case_sentenceContext)_localctx).sent_type = match(T__41);
				setState(262);
				((Case_sentenceContext)_localctx).expr = expression(0);
				setState(263);
				match(T__42);
				setState(267);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,28,_ctx);
				while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
					if ( _alt==1 ) {
						{
						{
						setState(264);
						((Case_sentenceContext)_localctx).sentence = sentence();
						((Case_sentenceContext)_localctx).sentences.add(((Case_sentenceContext)_localctx).sentence);
						}
						} 
					}
					setState(269);
					_errHandler.sync(this);
					_alt = getInterpreter().adaptivePredict(_input,28,_ctx);
				}
				setState(270);
				match(T__39);
				setState(271);
				match(T__4);
				}
				break;
			case T__43:
				enterOuterAlt(_localctx, 2);
				{
				setState(273);
				((Case_sentenceContext)_localctx).sent_type = match(T__43);
				setState(274);
				match(T__42);
				setState(278);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,29,_ctx);
				while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
					if ( _alt==1 ) {
						{
						{
						setState(275);
						((Case_sentenceContext)_localctx).sentence = sentence();
						((Case_sentenceContext)_localctx).sentences.add(((Case_sentenceContext)_localctx).sentence);
						}
						} 
					}
					setState(280);
					_errHandler.sync(this);
					_alt = getInterpreter().adaptivePredict(_input,29,_ctx);
				}
				setState(281);
				match(T__39);
				setState(282);
				match(T__4);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ExpressionContext extends ParserRuleContext {
		public ExpressionContext expr;
		public ExpressionContext array_name;
		public ExpressionContext left;
		public ExpressionContext r_expr;
		public Function_callContext f_call;
		public Token operator;
		public ExpressionContext right;
		public ExpressionContext index;
		public TerminalNode HEX_CONST() { return getToken(ArduinoParser.HEX_CONST, 0); }
		public TerminalNode OCTAL_CONST() { return getToken(ArduinoParser.OCTAL_CONST, 0); }
		public TerminalNode BINARY_CONST() { return getToken(ArduinoParser.BINARY_CONST, 0); }
		public TerminalNode INT_CONST() { return getToken(ArduinoParser.INT_CONST, 0); }
		public TerminalNode FLOAT_CONST() { return getToken(ArduinoParser.FLOAT_CONST, 0); }
		public TerminalNode CHAR_CONST() { return getToken(ArduinoParser.CHAR_CONST, 0); }
		public TerminalNode STRING_CONST() { return getToken(ArduinoParser.STRING_CONST, 0); }
		public TerminalNode ID() { return getToken(ArduinoParser.ID, 0); }
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public Function_callContext function_call() {
			return getRuleContext(Function_callContext.class,0);
		}
		public TerminalNode BIT_SHIFT_R() { return getToken(ArduinoParser.BIT_SHIFT_R, 0); }
		public TerminalNode BIT_SHIFT_L() { return getToken(ArduinoParser.BIT_SHIFT_L, 0); }
		public ExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expression; }
	}

	public final ExpressionContext expression() throws RecognitionException {
		return expression(0);
	}

	private ExpressionContext expression(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		ExpressionContext _localctx = new ExpressionContext(_ctx, _parentState);
		ExpressionContext _prevctx = _localctx;
		int _startState = 38;
		enterRecursionRule(_localctx, 38, RULE_expression, _p);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(305);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,31,_ctx) ) {
			case 1:
				{
				setState(286);
				match(T__44);
				}
				break;
			case 2:
				{
				setState(287);
				match(T__45);
				}
				break;
			case 3:
				{
				setState(288);
				match(HEX_CONST);
				}
				break;
			case 4:
				{
				setState(289);
				match(OCTAL_CONST);
				}
				break;
			case 5:
				{
				setState(290);
				match(BINARY_CONST);
				}
				break;
			case 6:
				{
				setState(291);
				match(INT_CONST);
				}
				break;
			case 7:
				{
				setState(292);
				match(FLOAT_CONST);
				}
				break;
			case 8:
				{
				setState(293);
				match(CHAR_CONST);
				}
				break;
			case 9:
				{
				setState(294);
				match(STRING_CONST);
				}
				break;
			case 10:
				{
				setState(295);
				match(ID);
				}
				break;
			case 11:
				{
				setState(296);
				match(T__30);
				setState(297);
				((ExpressionContext)_localctx).r_expr = expression(0);
				setState(298);
				match(T__31);
				}
				break;
			case 12:
				{
				setState(300);
				((ExpressionContext)_localctx).f_call = function_call();
				}
				break;
			case 13:
				{
				setState(301);
				((ExpressionContext)_localctx).operator = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==T__46 || _la==T__47) ) {
					((ExpressionContext)_localctx).operator = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(302);
				((ExpressionContext)_localctx).expr = expression(14);
				}
				break;
			case 14:
				{
				setState(303);
				((ExpressionContext)_localctx).operator = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==T__48 || _la==T__49) ) {
					((ExpressionContext)_localctx).operator = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(304);
				((ExpressionContext)_localctx).expr = expression(12);
				}
				break;
			}
			_ctx.stop = _input.LT(-1);
			setState(349);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,33,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(347);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,32,_ctx) ) {
					case 1:
						{
						_localctx = new ExpressionContext(_parentctx, _parentState);
						_localctx.left = _prevctx;
						_localctx.left = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_expression);
						setState(307);
						if (!(precpred(_ctx, 11))) throw new FailedPredicateException(this, "precpred(_ctx, 11)");
						setState(308);
						((ExpressionContext)_localctx).operator = _input.LT(1);
						_la = _input.LA(1);
						if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__50) | (1L << T__51) | (1L << T__52))) != 0)) ) {
							((ExpressionContext)_localctx).operator = (Token)_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(309);
						((ExpressionContext)_localctx).right = expression(12);
						}
						break;
					case 2:
						{
						_localctx = new ExpressionContext(_parentctx, _parentState);
						_localctx.left = _prevctx;
						_localctx.left = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_expression);
						setState(310);
						if (!(precpred(_ctx, 10))) throw new FailedPredicateException(this, "precpred(_ctx, 10)");
						setState(311);
						((ExpressionContext)_localctx).operator = _input.LT(1);
						_la = _input.LA(1);
						if ( !(_la==T__53 || _la==T__54) ) {
							((ExpressionContext)_localctx).operator = (Token)_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(312);
						((ExpressionContext)_localctx).right = expression(11);
						}
						break;
					case 3:
						{
						_localctx = new ExpressionContext(_parentctx, _parentState);
						_localctx.left = _prevctx;
						_localctx.left = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_expression);
						setState(313);
						if (!(precpred(_ctx, 9))) throw new FailedPredicateException(this, "precpred(_ctx, 9)");
						setState(314);
						((ExpressionContext)_localctx).operator = _input.LT(1);
						_la = _input.LA(1);
						if ( !(_la==BIT_SHIFT_L || _la==BIT_SHIFT_R) ) {
							((ExpressionContext)_localctx).operator = (Token)_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(315);
						((ExpressionContext)_localctx).right = expression(10);
						}
						break;
					case 4:
						{
						_localctx = new ExpressionContext(_parentctx, _parentState);
						_localctx.left = _prevctx;
						_localctx.left = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_expression);
						setState(316);
						if (!(precpred(_ctx, 8))) throw new FailedPredicateException(this, "precpred(_ctx, 8)");
						setState(317);
						((ExpressionContext)_localctx).operator = _input.LT(1);
						_la = _input.LA(1);
						if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__1) | (1L << T__3) | (1L << T__55) | (1L << T__56))) != 0)) ) {
							((ExpressionContext)_localctx).operator = (Token)_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(318);
						((ExpressionContext)_localctx).right = expression(9);
						}
						break;
					case 5:
						{
						_localctx = new ExpressionContext(_parentctx, _parentState);
						_localctx.left = _prevctx;
						_localctx.left = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_expression);
						setState(319);
						if (!(precpred(_ctx, 7))) throw new FailedPredicateException(this, "precpred(_ctx, 7)");
						setState(320);
						((ExpressionContext)_localctx).operator = _input.LT(1);
						_la = _input.LA(1);
						if ( !(_la==T__57 || _la==T__58) ) {
							((ExpressionContext)_localctx).operator = (Token)_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(321);
						((ExpressionContext)_localctx).right = expression(8);
						}
						break;
					case 6:
						{
						_localctx = new ExpressionContext(_parentctx, _parentState);
						_localctx.left = _prevctx;
						_localctx.left = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_expression);
						setState(322);
						if (!(precpred(_ctx, 6))) throw new FailedPredicateException(this, "precpred(_ctx, 6)");
						setState(323);
						((ExpressionContext)_localctx).operator = match(T__59);
						setState(324);
						((ExpressionContext)_localctx).right = expression(7);
						}
						break;
					case 7:
						{
						_localctx = new ExpressionContext(_parentctx, _parentState);
						_localctx.left = _prevctx;
						_localctx.left = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_expression);
						setState(325);
						if (!(precpred(_ctx, 5))) throw new FailedPredicateException(this, "precpred(_ctx, 5)");
						setState(326);
						((ExpressionContext)_localctx).operator = match(T__60);
						setState(327);
						((ExpressionContext)_localctx).right = expression(6);
						}
						break;
					case 8:
						{
						_localctx = new ExpressionContext(_parentctx, _parentState);
						_localctx.left = _prevctx;
						_localctx.left = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_expression);
						setState(328);
						if (!(precpred(_ctx, 4))) throw new FailedPredicateException(this, "precpred(_ctx, 4)");
						setState(329);
						((ExpressionContext)_localctx).operator = match(T__61);
						setState(330);
						((ExpressionContext)_localctx).right = expression(5);
						}
						break;
					case 9:
						{
						_localctx = new ExpressionContext(_parentctx, _parentState);
						_localctx.left = _prevctx;
						_localctx.left = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_expression);
						setState(331);
						if (!(precpred(_ctx, 3))) throw new FailedPredicateException(this, "precpred(_ctx, 3)");
						setState(332);
						((ExpressionContext)_localctx).operator = match(T__62);
						setState(333);
						((ExpressionContext)_localctx).right = expression(4);
						}
						break;
					case 10:
						{
						_localctx = new ExpressionContext(_parentctx, _parentState);
						_localctx.left = _prevctx;
						_localctx.left = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_expression);
						setState(334);
						if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
						setState(335);
						((ExpressionContext)_localctx).operator = match(T__63);
						setState(336);
						((ExpressionContext)_localctx).right = expression(3);
						}
						break;
					case 11:
						{
						_localctx = new ExpressionContext(_parentctx, _parentState);
						_localctx.left = _prevctx;
						_localctx.left = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_expression);
						setState(337);
						if (!(precpred(_ctx, 1))) throw new FailedPredicateException(this, "precpred(_ctx, 1)");
						setState(338);
						((ExpressionContext)_localctx).operator = _input.LT(1);
						_la = _input.LA(1);
						if ( !(((((_la - 65)) & ~0x3f) == 0 && ((1L << (_la - 65)) & ((1L << (T__64 - 65)) | (1L << (T__65 - 65)) | (1L << (T__66 - 65)) | (1L << (T__67 - 65)) | (1L << (T__68 - 65)) | (1L << (T__69 - 65)) | (1L << (T__70 - 65)) | (1L << (T__71 - 65)))) != 0)) ) {
							((ExpressionContext)_localctx).operator = (Token)_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(339);
						((ExpressionContext)_localctx).right = expression(2);
						}
						break;
					case 12:
						{
						_localctx = new ExpressionContext(_parentctx, _parentState);
						_localctx.expr = _prevctx;
						_localctx.expr = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_expression);
						setState(340);
						if (!(precpred(_ctx, 15))) throw new FailedPredicateException(this, "precpred(_ctx, 15)");
						setState(341);
						((ExpressionContext)_localctx).operator = _input.LT(1);
						_la = _input.LA(1);
						if ( !(_la==T__46 || _la==T__47) ) {
							((ExpressionContext)_localctx).operator = (Token)_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						}
						break;
					case 13:
						{
						_localctx = new ExpressionContext(_parentctx, _parentState);
						_localctx.array_name = _prevctx;
						_localctx.array_name = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_expression);
						setState(342);
						if (!(precpred(_ctx, 13))) throw new FailedPredicateException(this, "precpred(_ctx, 13)");
						setState(343);
						match(T__9);
						setState(344);
						((ExpressionContext)_localctx).index = expression(0);
						setState(345);
						match(T__10);
						}
						break;
					}
					} 
				}
				setState(351);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,33,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	public static class Function_callContext extends ParserRuleContext {
		public Token obj;
		public Token ID;
		public List<Token> elems = new ArrayList<Token>();
		public Function_callContext f_call;
		public Token f_name;
		public ParameterContext args;
		public List<TerminalNode> ID() { return getTokens(ArduinoParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(ArduinoParser.ID, i);
		}
		public Function_callContext function_call() {
			return getRuleContext(Function_callContext.class,0);
		}
		public ParameterContext parameter() {
			return getRuleContext(ParameterContext.class,0);
		}
		public Function_callContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_function_call; }
	}

	public final Function_callContext function_call() throws RecognitionException {
		Function_callContext _localctx = new Function_callContext(_ctx, getState());
		enterRule(_localctx, 40, RULE_function_call);
		int _la;
		try {
			int _alt;
			setState(368);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,36,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(352);
				((Function_callContext)_localctx).obj = match(ID);
				setState(357);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,34,_ctx);
				while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
					if ( _alt==1 ) {
						{
						{
						setState(353);
						match(T__2);
						setState(354);
						((Function_callContext)_localctx).ID = match(ID);
						((Function_callContext)_localctx).elems.add(((Function_callContext)_localctx).ID);
						}
						} 
					}
					setState(359);
					_errHandler.sync(this);
					_alt = getInterpreter().adaptivePredict(_input,34,_ctx);
				}
				setState(360);
				match(T__2);
				setState(361);
				((Function_callContext)_localctx).f_call = function_call();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(362);
				((Function_callContext)_localctx).f_name = match(ID);
				setState(363);
				match(T__30);
				setState(365);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (((((_la - 31)) & ~0x3f) == 0 && ((1L << (_la - 31)) & ((1L << (T__30 - 31)) | (1L << (T__44 - 31)) | (1L << (T__45 - 31)) | (1L << (T__46 - 31)) | (1L << (T__47 - 31)) | (1L << (T__48 - 31)) | (1L << (T__49 - 31)) | (1L << (BINARY_CONST - 31)) | (1L << (OCTAL_CONST - 31)) | (1L << (HEX_CONST - 31)) | (1L << (INT_CONST - 31)) | (1L << (FLOAT_CONST - 31)) | (1L << (CHAR_CONST - 31)) | (1L << (STRING_CONST - 31)) | (1L << (ID - 31)))) != 0)) {
					{
					setState(364);
					((Function_callContext)_localctx).args = parameter();
					}
				}

				setState(367);
				match(T__31);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ParameterContext extends ParserRuleContext {
		public ExpressionContext expression;
		public List<ExpressionContext> parameters = new ArrayList<ExpressionContext>();
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public ParameterContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_parameter; }
	}

	public final ParameterContext parameter() throws RecognitionException {
		ParameterContext _localctx = new ParameterContext(_ctx, getState());
		enterRule(_localctx, 42, RULE_parameter);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(370);
			((ParameterContext)_localctx).expression = expression(0);
			((ParameterContext)_localctx).parameters.add(((ParameterContext)_localctx).expression);
			setState(375);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__12) {
				{
				{
				setState(371);
				match(T__12);
				setState(372);
				((ParameterContext)_localctx).expression = expression(0);
				((ParameterContext)_localctx).parameters.add(((ParameterContext)_localctx).expression);
				}
				}
				setState(377);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 19:
			return expression_sempred((ExpressionContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean expression_sempred(ExpressionContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 11);
		case 1:
			return precpred(_ctx, 10);
		case 2:
			return precpred(_ctx, 9);
		case 3:
			return precpred(_ctx, 8);
		case 4:
			return precpred(_ctx, 7);
		case 5:
			return precpred(_ctx, 6);
		case 6:
			return precpred(_ctx, 5);
		case 7:
			return precpred(_ctx, 4);
		case 8:
			return precpred(_ctx, 3);
		case 9:
			return precpred(_ctx, 2);
		case 10:
			return precpred(_ctx, 1);
		case 11:
			return precpred(_ctx, 15);
		case 12:
			return precpred(_ctx, 13);
		}
		return true;
	}

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3Y\u017d\4\2\t\2\4"+
		"\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t"+
		"\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\3\2\3\2\3\2\3\3\7\3"+
		"\63\n\3\f\3\16\3\66\13\3\3\3\7\39\n\3\f\3\16\3<\13\3\3\4\3\4\3\4\3\4\3"+
		"\4\3\4\3\4\3\4\5\4F\n\4\3\5\3\5\3\5\3\5\3\5\5\5M\n\5\3\6\3\6\3\6\3\6\5"+
		"\6S\n\6\3\7\3\7\3\7\3\7\5\7Y\n\7\3\b\3\b\3\b\3\b\3\b\3\b\5\ba\n\b\5\b"+
		"c\n\b\3\t\3\t\3\t\3\t\3\t\3\t\5\tk\n\t\3\n\3\n\5\no\n\n\3\n\3\n\3\n\3"+
		"\n\7\nu\n\n\f\n\16\nx\13\n\3\13\3\13\3\13\3\13\6\13~\n\13\r\13\16\13\177"+
		"\3\13\3\13\3\13\3\13\3\13\3\13\7\13\u0088\n\13\f\13\16\13\u008b\13\13"+
		"\3\13\3\13\5\13\u008f\n\13\3\f\3\f\3\r\3\r\3\r\3\r\5\r\u0097\n\r\3\r\3"+
		"\r\3\r\7\r\u009c\n\r\f\r\16\r\u009f\13\r\3\r\3\r\3\16\3\16\3\16\7\16\u00a6"+
		"\n\16\f\16\16\16\u00a9\13\16\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3"+
		"\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\5\17\u00bc\n\17\3\17\3\17"+
		"\5\17\u00c0\n\17\3\17\3\17\5\17\u00c4\n\17\3\17\3\17\5\17\u00c8\n\17\3"+
		"\20\3\20\3\20\3\20\3\20\3\20\3\20\5\20\u00d1\n\20\3\20\3\20\3\20\3\20"+
		"\3\20\3\20\7\20\u00d9\n\20\f\20\16\20\u00dc\13\20\3\20\3\20\5\20\u00e0"+
		"\n\20\3\21\3\21\7\21\u00e4\n\21\f\21\16\21\u00e7\13\21\3\21\3\21\5\21"+
		"\u00eb\n\21\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22"+
		"\3\22\3\22\5\22\u00fb\n\22\3\22\3\22\3\22\3\22\3\22\5\22\u0102\n\22\3"+
		"\23\3\23\3\23\3\23\3\24\3\24\3\24\3\24\7\24\u010c\n\24\f\24\16\24\u010f"+
		"\13\24\3\24\3\24\3\24\3\24\3\24\3\24\7\24\u0117\n\24\f\24\16\24\u011a"+
		"\13\24\3\24\3\24\5\24\u011e\n\24\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3"+
		"\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\5\25\u0134"+
		"\n\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25"+
		"\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25"+
		"\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\7\25"+
		"\u015e\n\25\f\25\16\25\u0161\13\25\3\26\3\26\3\26\7\26\u0166\n\26\f\26"+
		"\16\26\u0169\13\26\3\26\3\26\3\26\3\26\3\26\5\26\u0170\n\26\3\26\5\26"+
		"\u0173\n\26\3\27\3\27\3\27\7\27\u0178\n\27\f\27\16\27\u017b\13\27\3\27"+
		"\2\3(\30\2\4\6\b\n\f\16\20\22\24\26\30\32\34\36 \"$&(*,\2\f\3\2\b\t\4"+
		"\2\21 VV\3\2\61\62\3\2\63\64\3\2\65\67\3\289\3\2KL\5\2\4\4\6\6:;\3\2<"+
		"=\3\2CJ\2\u01ad\2.\3\2\2\2\4\64\3\2\2\2\6E\3\2\2\2\bL\3\2\2\2\nR\3\2\2"+
		"\2\fT\3\2\2\2\16Z\3\2\2\2\20j\3\2\2\2\22l\3\2\2\2\24\u008e\3\2\2\2\26"+
		"\u0090\3\2\2\2\30\u0092\3\2\2\2\32\u00a2\3\2\2\2\34\u00c7\3\2\2\2\36\u00df"+
		"\3\2\2\2 \u00ea\3\2\2\2\"\u0101\3\2\2\2$\u0103\3\2\2\2&\u011d\3\2\2\2"+
		"(\u0133\3\2\2\2*\u0172\3\2\2\2,\u0174\3\2\2\2./\5\4\3\2/\60\7\2\2\3\60"+
		"\3\3\2\2\2\61\63\5\6\4\2\62\61\3\2\2\2\63\66\3\2\2\2\64\62\3\2\2\2\64"+
		"\65\3\2\2\2\65:\3\2\2\2\66\64\3\2\2\2\679\5\b\5\28\67\3\2\2\29<\3\2\2"+
		"\2:8\3\2\2\2:;\3\2\2\2;\5\3\2\2\2<:\3\2\2\2=>\7\3\2\2>F\7T\2\2?@\7\3\2"+
		"\2@A\7\4\2\2AB\7V\2\2BC\7\5\2\2CD\7V\2\2DF\7\6\2\2E=\3\2\2\2E?\3\2\2\2"+
		"F\7\3\2\2\2GH\5\n\6\2HI\7\7\2\2IM\3\2\2\2JM\5\30\r\2KM\5\20\t\2LG\3\2"+
		"\2\2LJ\3\2\2\2LK\3\2\2\2M\t\3\2\2\2NS\5\f\7\2OS\5\16\b\2PQ\t\2\2\2QS\5"+
		"\n\6\2RN\3\2\2\2RO\3\2\2\2RP\3\2\2\2S\13\3\2\2\2TU\5\26\f\2UX\7V\2\2V"+
		"W\7\n\2\2WY\5(\25\2XV\3\2\2\2XY\3\2\2\2Y\r\3\2\2\2Z[\5\26\f\2[\\\7V\2"+
		"\2\\b\5\22\n\2]`\7\n\2\2^a\5(\25\2_a\5\24\13\2`^\3\2\2\2`_\3\2\2\2ac\3"+
		"\2\2\2b]\3\2\2\2bc\3\2\2\2c\17\3\2\2\2de\7\13\2\2ef\7V\2\2fk\5(\25\2g"+
		"h\7\13\2\2hi\7V\2\2ik\5\24\13\2jd\3\2\2\2jg\3\2\2\2k\21\3\2\2\2ln\7\f"+
		"\2\2mo\7P\2\2nm\3\2\2\2no\3\2\2\2op\3\2\2\2pv\7\r\2\2qr\7\f\2\2rs\7P\2"+
		"\2su\7\r\2\2tq\3\2\2\2ux\3\2\2\2vt\3\2\2\2vw\3\2\2\2w\23\3\2\2\2xv\3\2"+
		"\2\2yz\7\16\2\2z}\5\24\13\2{|\7\17\2\2|~\5\24\13\2}{\3\2\2\2~\177\3\2"+
		"\2\2\177}\3\2\2\2\177\u0080\3\2\2\2\u0080\u0081\3\2\2\2\u0081\u0082\7"+
		"\20\2\2\u0082\u008f\3\2\2\2\u0083\u0084\7\16\2\2\u0084\u0089\5(\25\2\u0085"+
		"\u0086\7\17\2\2\u0086\u0088\5(\25\2\u0087\u0085\3\2\2\2\u0088\u008b\3"+
		"\2\2\2\u0089\u0087\3\2\2\2\u0089\u008a\3\2\2\2\u008a\u008c\3\2\2\2\u008b"+
		"\u0089\3\2\2\2\u008c\u008d\7\20\2\2\u008d\u008f\3\2\2\2\u008ey\3\2\2\2"+
		"\u008e\u0083\3\2\2\2\u008f\25\3\2\2\2\u0090\u0091\t\3\2\2\u0091\27\3\2"+
		"\2\2\u0092\u0093\5\26\f\2\u0093\u0094\7V\2\2\u0094\u0096\7!\2\2\u0095"+
		"\u0097\5\32\16\2\u0096\u0095\3\2\2\2\u0096\u0097\3\2\2\2\u0097\u0098\3"+
		"\2\2\2\u0098\u0099\7\"\2\2\u0099\u009d\7\16\2\2\u009a\u009c\5\"\22\2\u009b"+
		"\u009a\3\2\2\2\u009c\u009f\3\2\2\2\u009d\u009b\3\2\2\2\u009d\u009e\3\2"+
		"\2\2\u009e\u00a0\3\2\2\2\u009f\u009d\3\2\2\2\u00a0\u00a1\7\20\2\2\u00a1"+
		"\31\3\2\2\2\u00a2\u00a7\5\n\6\2\u00a3\u00a4\7\17\2\2\u00a4\u00a6\5\n\6"+
		"\2\u00a5\u00a3\3\2\2\2\u00a6\u00a9\3\2\2\2\u00a7\u00a5\3\2\2\2\u00a7\u00a8"+
		"\3\2\2\2\u00a8\33\3\2\2\2\u00a9\u00a7\3\2\2\2\u00aa\u00ab\7#\2\2\u00ab"+
		"\u00ac\7!\2\2\u00ac\u00ad\5(\25\2\u00ad\u00ae\7\"\2\2\u00ae\u00af\5 \21"+
		"\2\u00af\u00c8\3\2\2\2\u00b0\u00b1\7$\2\2\u00b1\u00b2\5 \21\2\u00b2\u00b3"+
		"\7#\2\2\u00b3\u00b4\7!\2\2\u00b4\u00b5\5(\25\2\u00b5\u00b6\7\"\2\2\u00b6"+
		"\u00b7\7\7\2\2\u00b7\u00c8\3\2\2\2\u00b8\u00b9\7%\2\2\u00b9\u00bb\7!\2"+
		"\2\u00ba\u00bc\5\f\7\2\u00bb\u00ba\3\2\2\2\u00bb\u00bc\3\2\2\2\u00bc\u00bd"+
		"\3\2\2\2\u00bd\u00bf\7\7\2\2\u00be\u00c0\5(\25\2\u00bf\u00be\3\2\2\2\u00bf"+
		"\u00c0\3\2\2\2\u00c0\u00c1\3\2\2\2\u00c1\u00c3\7\7\2\2\u00c2\u00c4\5("+
		"\25\2\u00c3\u00c2\3\2\2\2\u00c3\u00c4\3\2\2\2\u00c4\u00c5\3\2\2\2\u00c5"+
		"\u00c6\7\"\2\2\u00c6\u00c8\5 \21\2\u00c7\u00aa\3\2\2\2\u00c7\u00b0\3\2"+
		"\2\2\u00c7\u00b8\3\2\2\2\u00c8\35\3\2\2\2\u00c9\u00ca\7&\2\2\u00ca\u00cb"+
		"\7!\2\2\u00cb\u00cc\5(\25\2\u00cc\u00cd\7\"\2\2\u00cd\u00d0\5 \21\2\u00ce"+
		"\u00cf\7\'\2\2\u00cf\u00d1\5 \21\2\u00d0\u00ce\3\2\2\2\u00d0\u00d1\3\2"+
		"\2\2\u00d1\u00e0\3\2\2\2\u00d2\u00d3\7(\2\2\u00d3\u00d4\7!\2\2\u00d4\u00d5"+
		"\5(\25\2\u00d5\u00d6\7\"\2\2\u00d6\u00da\7\16\2\2\u00d7\u00d9\5&\24\2"+
		"\u00d8\u00d7\3\2\2\2\u00d9\u00dc\3\2\2\2\u00da\u00d8\3\2\2\2\u00da\u00db"+
		"\3\2\2\2\u00db\u00dd\3\2\2\2\u00dc\u00da\3\2\2\2\u00dd\u00de\7\20\2\2"+
		"\u00de\u00e0\3\2\2\2\u00df\u00c9\3\2\2\2\u00df\u00d2\3\2\2\2\u00e0\37"+
		"\3\2\2\2\u00e1\u00e5\7\16\2\2\u00e2\u00e4\5\"\22\2\u00e3\u00e2\3\2\2\2"+
		"\u00e4\u00e7\3\2\2\2\u00e5\u00e3\3\2\2\2\u00e5\u00e6\3\2\2\2\u00e6\u00e8"+
		"\3\2\2\2\u00e7\u00e5\3\2\2\2\u00e8\u00eb\7\20\2\2\u00e9\u00eb\5\"\22\2"+
		"\u00ea\u00e1\3\2\2\2\u00ea\u00e9\3\2\2\2\u00eb!\3\2\2\2\u00ec\u00ed\5"+
		"\n\6\2\u00ed\u00ee\7\7\2\2\u00ee\u0102\3\2\2\2\u00ef\u0102\5\34\17\2\u00f0"+
		"\u0102\5\36\20\2\u00f1\u00f2\5$\23\2\u00f2\u00f3\7\7\2\2\u00f3\u0102\3"+
		"\2\2\2\u00f4\u00f5\5(\25\2\u00f5\u00f6\7\7\2\2\u00f6\u0102\3\2\2\2\u00f7"+
		"\u0102\5\20\t\2\u00f8\u00fa\7)\2\2\u00f9\u00fb\5(\25\2\u00fa\u00f9\3\2"+
		"\2\2\u00fa\u00fb\3\2\2\2\u00fb\u00fc\3\2\2\2\u00fc\u0102\7\7\2\2\u00fd"+
		"\u00fe\7*\2\2\u00fe\u0102\7\7\2\2\u00ff\u0100\7+\2\2\u0100\u0102\7\7\2"+
		"\2\u0101\u00ec\3\2\2\2\u0101\u00ef\3\2\2\2\u0101\u00f0\3\2\2\2\u0101\u00f1"+
		"\3\2\2\2\u0101\u00f4\3\2\2\2\u0101\u00f7\3\2\2\2\u0101\u00f8\3\2\2\2\u0101"+
		"\u00fd\3\2\2\2\u0101\u00ff\3\2\2\2\u0102#\3\2\2\2\u0103\u0104\5(\25\2"+
		"\u0104\u0105\7\n\2\2\u0105\u0106\5(\25\2\u0106%\3\2\2\2\u0107\u0108\7"+
		",\2\2\u0108\u0109\5(\25\2\u0109\u010d\7-\2\2\u010a\u010c\5\"\22\2\u010b"+
		"\u010a\3\2\2\2\u010c\u010f\3\2\2\2\u010d\u010b\3\2\2\2\u010d\u010e\3\2"+
		"\2\2\u010e\u0110\3\2\2\2\u010f\u010d\3\2\2\2\u0110\u0111\7*\2\2\u0111"+
		"\u0112\7\7\2\2\u0112\u011e\3\2\2\2\u0113\u0114\7.\2\2\u0114\u0118\7-\2"+
		"\2\u0115\u0117\5\"\22\2\u0116\u0115\3\2\2\2\u0117\u011a\3\2\2\2\u0118"+
		"\u0116\3\2\2\2\u0118\u0119\3\2\2\2\u0119\u011b\3\2\2\2\u011a\u0118\3\2"+
		"\2\2\u011b\u011c\7*\2\2\u011c\u011e\7\7\2\2\u011d\u0107\3\2\2\2\u011d"+
		"\u0113\3\2\2\2\u011e\'\3\2\2\2\u011f\u0120\b\25\1\2\u0120\u0134\7/\2\2"+
		"\u0121\u0134\7\60\2\2\u0122\u0134\7O\2\2\u0123\u0134\7N\2\2\u0124\u0134"+
		"\7M\2\2\u0125\u0134\7P\2\2\u0126\u0134\7Q\2\2\u0127\u0134\7R\2\2\u0128"+
		"\u0134\7T\2\2\u0129\u0134\7V\2\2\u012a\u012b\7!\2\2\u012b\u012c\5(\25"+
		"\2\u012c\u012d\7\"\2\2\u012d\u0134\3\2\2\2\u012e\u0134\5*\26\2\u012f\u0130"+
		"\t\4\2\2\u0130\u0134\5(\25\20\u0131\u0132\t\5\2\2\u0132\u0134\5(\25\16"+
		"\u0133\u011f\3\2\2\2\u0133\u0121\3\2\2\2\u0133\u0122\3\2\2\2\u0133\u0123"+
		"\3\2\2\2\u0133\u0124\3\2\2\2\u0133\u0125\3\2\2\2\u0133\u0126\3\2\2\2\u0133"+
		"\u0127\3\2\2\2\u0133\u0128\3\2\2\2\u0133\u0129\3\2\2\2\u0133\u012a\3\2"+
		"\2\2\u0133\u012e\3\2\2\2\u0133\u012f\3\2\2\2\u0133\u0131\3\2\2\2\u0134"+
		"\u015f\3\2\2\2\u0135\u0136\f\r\2\2\u0136\u0137\t\6\2\2\u0137\u015e\5("+
		"\25\16\u0138\u0139\f\f\2\2\u0139\u013a\t\7\2\2\u013a\u015e\5(\25\r\u013b"+
		"\u013c\f\13\2\2\u013c\u013d\t\b\2\2\u013d\u015e\5(\25\f\u013e\u013f\f"+
		"\n\2\2\u013f\u0140\t\t\2\2\u0140\u015e\5(\25\13\u0141\u0142\f\t\2\2\u0142"+
		"\u0143\t\n\2\2\u0143\u015e\5(\25\n\u0144\u0145\f\b\2\2\u0145\u0146\7>"+
		"\2\2\u0146\u015e\5(\25\t\u0147\u0148\f\7\2\2\u0148\u0149\7?\2\2\u0149"+
		"\u015e\5(\25\b\u014a\u014b\f\6\2\2\u014b\u014c\7@\2\2\u014c\u015e\5(\25"+
		"\7\u014d\u014e\f\5\2\2\u014e\u014f\7A\2\2\u014f\u015e\5(\25\6\u0150\u0151"+
		"\f\4\2\2\u0151\u0152\7B\2\2\u0152\u015e\5(\25\5\u0153\u0154\f\3\2\2\u0154"+
		"\u0155\t\13\2\2\u0155\u015e\5(\25\4\u0156\u0157\f\21\2\2\u0157\u015e\t"+
		"\4\2\2\u0158\u0159\f\17\2\2\u0159\u015a\7\f\2\2\u015a\u015b\5(\25\2\u015b"+
		"\u015c\7\r\2\2\u015c\u015e\3\2\2\2\u015d\u0135\3\2\2\2\u015d\u0138\3\2"+
		"\2\2\u015d\u013b\3\2\2\2\u015d\u013e\3\2\2\2\u015d\u0141\3\2\2\2\u015d"+
		"\u0144\3\2\2\2\u015d\u0147\3\2\2\2\u015d\u014a\3\2\2\2\u015d\u014d\3\2"+
		"\2\2\u015d\u0150\3\2\2\2\u015d\u0153\3\2\2\2\u015d\u0156\3\2\2\2\u015d"+
		"\u0158\3\2\2\2\u015e\u0161\3\2\2\2\u015f\u015d\3\2\2\2\u015f\u0160\3\2"+
		"\2\2\u0160)\3\2\2\2\u0161\u015f\3\2\2\2\u0162\u0167\7V\2\2\u0163\u0164"+
		"\7\5\2\2\u0164\u0166\7V\2\2\u0165\u0163\3\2\2\2\u0166\u0169\3\2\2\2\u0167"+
		"\u0165\3\2\2\2\u0167\u0168\3\2\2\2\u0168\u016a\3\2\2\2\u0169\u0167\3\2"+
		"\2\2\u016a\u016b\7\5\2\2\u016b\u0173\5*\26\2\u016c\u016d\7V\2\2\u016d"+
		"\u016f\7!\2\2\u016e\u0170\5,\27\2\u016f\u016e\3\2\2\2\u016f\u0170\3\2"+
		"\2\2\u0170\u0171\3\2\2\2\u0171\u0173\7\"\2\2\u0172\u0162\3\2\2\2\u0172"+
		"\u016c\3\2\2\2\u0173+\3\2\2\2\u0174\u0179\5(\25\2\u0175\u0176\7\17\2\2"+
		"\u0176\u0178\5(\25\2\u0177\u0175\3\2\2\2\u0178\u017b\3\2\2\2\u0179\u0177"+
		"\3\2\2\2\u0179\u017a\3\2\2\2\u017a-\3\2\2\2\u017b\u0179\3\2\2\2(\64:E"+
		"LRX`bjnv\177\u0089\u008e\u0096\u009d\u00a7\u00bb\u00bf\u00c3\u00c7\u00d0"+
		"\u00da\u00df\u00e5\u00ea\u00fa\u0101\u010d\u0118\u011d\u0133\u015d\u015f"+
		"\u0167\u016f\u0172\u0179";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}