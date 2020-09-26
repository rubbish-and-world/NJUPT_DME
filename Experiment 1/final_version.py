import itertools
from prettytable import PrettyTable

class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def top(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

stack_op = Stack()
stack_obj = Stack()
neg = "¬"
disjunction = "∧"
conjunction =  "∨"
implies  = "→"
left = "("
right = ")"
symbols = {neg:" not " , conjunction:" or " , disjunction:" and " , implies:" ** ",left:"(",right:")"}
conls = []
disls = []

def count(enter,varls):
    ll = list(enter)
    for i in ll:
        if i not in symbols.keys() and i not in varls:
            varls.append(i)
    return len(varls)

def judge(fin_str):
    process = Stack()
    s = fin_str.split()
    for i in s:
        if i not in symbols.keys():
            process.push(i)
        elif i == neg:
            obj = process.pop()
            res = eval(symbols[i] + obj)
            process.push(str(res))
        else:
            obj1 = str(process.pop())
            obj2 = str(process.pop())
            res = eval(obj2 + symbols[i] + obj1)
            process.push(res)
    final = process.pop()
    return final

def choice(ls , repeating):
    first = ls
    second = first
    third = []
    for k in range(repeating-1):
        for i in first:
            for x in second:
                third.append(i+x)
        second = third.copy()
        third.clear()
    return second

def get_prime_con(vars , truths , result):
    unit = ""
    if result:
        unit = "("
        for index in range(len(truths)):
            if truths[index]:
                unit += vars[index]
            else:
                unit += neg + vars[index]
            if index != len(truths)-1:
                unit += disjunction
        unit += ")"
    return unit

def get_prime_dis(vars , truths , result):
    unit = ""
    if not result:
        unit = "("
        for index in range(len(truths)):
            if truths[index]:
                unit += neg + vars[index]
            else:
                unit += vars[index]
            if index != len(truths)-1:
                unit += conjunction
        unit+= ")"
    return unit

def convert(i):
    if i:
        return True
    else:
        return False

def make_truth_table(n,enter):
    table = choice([[True] , [False]] , n)
    # can be replaced with built-in module , 'list(__import__("itertools").product([True , False] , repeat = 3 ))'
    tb = PrettyTable()
    tb.field_names = vars
    for i in table:
        result = parse(enter , vars , i)
        tru_result = convert(eval(str(judge(result))))
        conls.append(get_prime_con(vars , i  , tru_result))
        disls.append(get_prime_dis(vars , i , tru_result))
        tb.add_row(i + [tru_result])
    print(tb)

# parse functions
def precedence(oper):
    if oper == neg:
        return 4
    elif oper == disjunction:
        return 3
    elif oper == conjunction:
        return 2
    elif oper == implies:
        return 1
    elif oper == left:
        return 0

def neg_out():
    obj = stack_obj.pop()
    oper = stack_op.pop()
    tail = obj + " " + oper
    return tail

def double_out():
    if stack_op.top() == neg:
        tail = neg_out()
    else:
        obj1 = stack_obj.pop()
        obj2 = stack_obj.pop()
        op = stack_op.pop()
        tail =  (obj1 + " " + obj2 + " " + op)
    return tail

def single_out():
    while not stack_obj.is_empty() and not stack_op.is_empty():
        if stack_op.top() == neg:
            op = stack_op.pop()
            tail = op
        else:
            obj = stack_obj.pop()
            op = stack_op.pop()
            tail =  (" " + obj + " " + op)
    return tail

def calcu(s):
    ls = s.split()
    op = ls[-1]
    if len(ls) == 3:
        obj1 = ls[0]
        obj2 = ls[1]
        if op == conjunction:
            result = eval(obj1) or eval(obj2)
        elif op == disjunction:
            result = eval(obj1) and eval(obj2)
        elif op == implies:
            result = eval(obj2) ** eval(obj1)

    elif len(ls) == 2 :
        obj = ls[0]
        result = eval(symbols[op] + obj)
    return  str(result)

def parse(enter , varls , i):
    for v in range(len(i)):
        exec(varls[v] + " = " +  str(i[v]) , globals())

    task = list(enter)
    behind = ""
    for x in task:
        if x not in symbols.keys():
            stack_obj.push(x)
        elif x == left:
            stack_op.push(x)
        elif x == right and not stack_op.is_empty():
            while stack_op.top() != left:
                if behind == "":
                    res = double_out()
                else:
                    res = single_out()
                stack_obj.push(calcu(res))
            stack_op.pop()
        else:
            if stack_op.is_empty():
                stack_op.push(x)
            elif precedence(x) >  precedence(stack_op.top()):
                stack_op.push(x)
            else:
                if behind == "":
                    res = double_out()
                else:
                    res = single_out()
                behind += res
                stack_op.push(x)
    tail = behind
    while not stack_op.is_empty() and not stack_obj.is_empty():
        if tail == "":
            tail += double_out()
        else:
            if stack_op.top() == neg:
                op = stack_op.pop()
                tail += (" "+ op +" ")
            else:
                obj = stack_obj.pop()
                op = stack_op.pop()
                tail +=  (" "+ (obj + " " + op)+" ")
    while not stack_op.is_empty():
        tail += (" "+ stack_op.pop()+" ")
    while not stack_obj.is_empty():
        tail += (" "+ stack_obj.pop()+" ")
    return tail

# end of parse functions

def make_prime(ls):
    ls = list(filter(None, ls))
    if len(ls) == 0:
        return "empty"
    if len(ls) == 1:
        return ls[0]
    res = ""
    if ls is conls:
        flag = disjunction
    else:
        flag = conjunction
    for i in ls[:-1]:
        if i:
            res += (i + flag)
    res += ls[-1]
    return res
try:
    vars = []
    enter = input("enter a formula:\n('P→¬(N∧R)' for instance)\n(parentheses nested in parentheses should be explicit like '(P∧Q)∨(¬P∧R∧S)' should be '(P∧Q)∨(((¬P)∧R)∧S)')\n")
    numb = count(enter , vars)
    vars.append(enter) # makr pretty_table field_names match rows
    make_truth_table(numb,enter)
    primary_con = make_prime(conls)
    primary_dis = make_prime(disls)
    print("The Primary Conjunctive normal form is : " , primary_con)
    print("The Primary Disjunctive normal form is : " , primary_dis)
except:
    print("invalid input.")

# it's funny: x ** y could be bool(x) <= bool(y) in python.
# mutiply objs in () without explicit parentheses will result in error ,but I don't know how to fix it ....... *_*
# and I don't know how to avoid using the 'eval()' and the 'exec()' functions , that's so bad ...........
# These codes writen by me are fucking shitty , fuck.
