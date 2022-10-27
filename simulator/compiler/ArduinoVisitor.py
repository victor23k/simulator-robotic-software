# Generated from E:\Asignaturas\Cuarto\TFG\SimuladorSoftwareRobots\simulator\compiler\Arduino.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ArduinoParser import ArduinoParser
else:
    from ArduinoParser import ArduinoParser

# This class defines a complete generic visitor for a parse tree produced by ArduinoParser.
def visitChildren(self, ctx):
    return self.visitChildren(ctx)


# this is the list of methods that we have to implement

List_of_methods = ['visitStart',
                   'visitProgram',
                   'visitInclude',
                   'visitProgram_code',
                   'visitDeclaration',
                   'visitSimple_declaration',
                   'visitArray_declaration',
                   'visitDefine_macro',
                   'visitArray_index',
                   'visitArray_elements',
                   'visitVar_type',
                   'visitFunction',
                   'visitFunction_args',
                   'visitIteration_sentence',
                   'visitConditional_sentence',
                   'visitCase_sentence',
                   'visitCode_block',
                   'visitSentence',
                   'visitAssignment',
                   'visitExpression',
                   'visitConversion',
                   'visitType_convert',
                   'visitParameter']


class ArduinoVisitor(ParseTreeVisitor):
    pass


for name in List_of_methods:
    setattr(ArduinoVisitor, name, visitChildren)



del ArduinoParser
