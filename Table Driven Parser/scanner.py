import re
import sys

user_input = input()
if len(user_input.split()) != 2:
    print("Please enter correct number of arguments: ")
    user_input = input()
else:
    first_word = user_input.split()[0]
    if first_word != 'scanner':
        print("Please enter 'scanner' as first argument: ")
        user_input = input()
       
filename = user_input.split()[1]

# table used to check nonterminals
parse_table = {'program' : {'id': 1, 'read': 1, 'write': 1, '$$': 1},
               'stmt_list' : {'id': 2, 'read': 2, 'write': 2, '$$': 3},
               'stmt' : {'id': 4, 'read': 5, 'write': 6},
               'expr' : {'id': 7, 'number': 7, '(': 7},
               'term_tail' : {'id': 9, 'read': 9, 'write': 9, ')': 9, '+': 8, '-': 8, '$$': 9},
               'term' : {'id': 10, 'number': 10, '(': 10},
               'factor_tail' : {'id': 12, 'read': 12, 'write': 12, ')': 12, '+': 12, '-': 12, '*': 11, '/': 11, '$$': 12},
               'factor' : {'id': 14, 'number': 15, '(': 13},
               'add_op' : {'+': 16, '-': 17},
               'mult_op' : {'*': 18, '/': 19}}

# table used to determine production rules
prod_rules = {1: ['stmt_list', '$$'],
              2: ['stmt', 'stmt_list'],
              3: [],
              4: ['id', ':=', 'expr'],
              5: ['read', 'id'],
              6: ['write', 'expr'],
              7: ['term', 'term_tail'],
              8: ['add_op', 'term', 'term_tail'],
              9: [],
              10: ['factor', 'factor_tail'],
              11: ['mult_op', 'factor', 'factor_tail'],
              12: [],
              13: ['(', 'expr', ')'],
              14: ['id'],
              15: ['number'],
              16: ['+'],
              17: ['-'],
              18: ['*'],
              19: ['/']}

# valid terminals in the input file
terminals = ['id', 'number', 'read', 'write', ':=', '(', ')', '+', '-', '*', '/', '$$']

def recognized_tokens(filename):

    # reads from file disregarding newline or tab
    # and puts it into a list.
    # joins list together and then creates new
    # list after removing comments
    input_stream = [ch for ch in open(filename).read() if ch != '\n' if ch != '\t']
    string = ''.join(input_stream)
    source = re.split(r'/\*.*?\*/', string)

    # splits list again at white spaces
    for i, num in enumerate(source):
        source[i] = num.split(' ')

    # creates new list splitting each element
    # and sets it to list 'source'
    raw_input = []
    for inner_lst in source:
        for ele in inner_lst:
            raw_input.append(re.findall(r"[\w']+|[\W']+", ele))

    source = raw_input

    # creates raw list of inputs and adds each element
    # from the source list
    final_list = []
    for inner_lst in source:
        for ele in inner_lst:
            final_list.append(ele)

    # creating new list with tokens identified
    tokens = []
    for element in final_list:
        if element in terminals:
            tokens.append(element)
        elif str(element).isdigit():
            tokens.append('number')
        elif element != 'read' or element != 'write':
            tokens.append('id')
        else:
            print("Token not recognized")
            sys.exit(1)

    return tokens

tokens = recognized_tokens(filename)
tokens.append('$$')

results = []

applied_prod = []

def scan(tokens):

    stack = ['program']

    i = 0
    
    try:

        # add exit token to stack
        # while stack is not empty
        stack.append('$$')
        while len(stack) > 0:
            current_token = tokens[i]
            top = stack.pop(0)
            if (isTerminal(top) and top == current_token):
                results.append(top)
                i = i + 1
                # print(results)
                continue
            elif top == ':=' and top != current_token:
                stack.pop(0)
                continue
            else:
                if current_token == '$$':
                    stack.pop(0)
                x = get_prod_rule(top, current_token)
                stack = x + stack
                print(stack)
                # print(applied_prod) #
                
    except IndexError:
        return results

# checks to see if top of stack is key of parse_table
def isTerminal(top):

    if top not in parse_table.keys():
        return True

# gets the next production rule to append to stack
def get_prod_rule(top, current_token):

    try:
        
        next_prod_num = parse_table[top][current_token]
        applied_prod.append(next_prod_num)
        new_rules = list(prod_rules[next_prod_num])
        return new_rules

    except KeyError:

        next_prod_num = recursive_lookup(current_token, parse_table)
        applied_prod.append(next_prod_num)
        new_rules = list(prod_rules[next_prod_num])
        return new_rules

# iterates through parse table to find terminal
# for next production rule
def recursive_lookup(key, table):

    if key in table:
        return table[key]
    for value in table.values():
        if isinstance(value, dict):
            a = recursive_lookup(key, value)
            if a is not None:
                return a

    return None

# prints tokens
def print_results():

    for i, word in  enumerate(results):
        if word == ':=':
            results[i] = 'assign'
        elif word == '(':
            results[i] = 'left parentheses'
        elif word == ')':
            results[i] = 'right parentheses'
        elif word == '+':
            results[i] = 'plus'
        elif word == '-':
            results[i] = 'minus'
        elif word == '*':
            results[i] = 'times'
        elif word == '/':
            results[i] = 'divide'
        elif word == '$$':
            results.remove('$$')

    formatted_results = ", ".join(results)
    print("({0})".format(formatted_results))  

scan(tokens)
print_results()

