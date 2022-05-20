from GUI.tree import TreeNodeDrawing
from parser.grammar import *
from parser.terminals import *

class Parser:

    def __init__(self,parsetreecanvas,start_rule):
        self.__parsetreecanvas = parsetreecanvas
        self.__start_rule = start_rule

    @staticmethod
    def join_list(input):
        str = ''
        for grammar in input[:]:
            if isinstance(grammar,TreeNodeDrawing):
                str += grammar.__repr__()
            else:
                str += grammar
        return str

    def __parse_input(self,input):
        tokens = []
        str = ''
        for char in input:
            if char == '+' or char == '-' or char == '*' or char == '/' or char == ')' or char == '(' :
                if str:
                    tokens.append(str)
                tokens.append(char)
                str = ''
            elif char != ' ':
                str+=char

        if str:
            tokens.append(str)
        tokens.append('$')
        return tokens

    def parse(self,input,action_table):
        terminals = []
        initial_exp = self.__start_rule(self.__parsetreecanvas,0,None,0,self.__parsetreecanvas.winfo_width())
        initial_exp.draw()
        stack = [initial_exp,'$']
        input = self.__parse_input(input)
        action = ''
        while len(input) >0:
            stack_state = Parser.join_list(stack)
            input_state = ''.join(input)
            rule = stack.pop(0)
            if isinstance(rule,Rule):
                rules =  rule.propagate(input[0])
                action = rule.__repr__() + '-->'
                for i in range(len(rules)):
                    action += rules[i].__repr__()
                    stack.insert(i,rules[i])
            elif isinstance(rule,EpsilonTerminal):
                action = 'remove epsilon'
                terminals.append(rule)
            else:
                terminals.append(rule)
                if(rule.__str__() == input[0]):
                    action = f'match , pop({input[0]})'
                    input.__delitem__(0)
                else:
                    action_table.append([stack_state,input_state,'Error terminals don\'t match'])
                    raise Exception()
            action_table.append([stack_state,input_state,action])

        return terminals[:-1]
