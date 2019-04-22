#programmer: Reid Reininger(charles.reininger@wsu.edu)
#date: 11/7/18
#desc: Intended for Unix/Linux Systems. Interpreter for Simplified
#      Postscript(SPS). Part2. Part2 code begins at line 272. Part2 test
#      functions begin at line 821.

#to check for iterable object types
from collections.abc import Iterable
import re

#globals
opstack = []
dictstack = []
gscope = ''

#operand stack operators
def opPop():
    """Pop opstack and return None on failure."""
    if len(opstack) >= 1:
        return opstack.pop()
    else:
        print('error: not enough items in opstack')

def opPush(value):
    """Push value onto opstack."""
    opstack.append(value)

def opPopn(n):
    """Pop n values from opstack and return as tuple or None on fail."""
    if len(opstack) >= n:
        return tuple(opPop() for x in range(n))
    else:
        print('error: not enough items in opstack')

#dictionary stack operators
def dictPop():
    """Pop dictstack and return None on failure."""
    if len(dictstack) >= 1:
        return dictstack.pop()
    else:
        print('error: not enough items in dictstack')

def dictPush(dictionary={}, chain=0):
    """Push empty dict onto dictstack by default and return False on failure."""
    if isinstance(dictionary, dict):
        dictstack.append((dictionary, chain))
        return True
    else:
        print('error: only dictionaries may be pushed to dictstack')
        return False

def define(name, value):
    """Add name:value pair to top dict in dictstack and return False on fail."""

    def isValidName(string):
        """Return true if string is a valid name."""
        if not isinstance(string, str):
            return False
        tests = []
        tests.append(string[0] == '/')
        tests.append(string[1].isalpha())
        tests.append(string[1:].isalnum())
        return all(tests)

    if isValidName(name):
        #if no dictionary in dictstack, push an empty one
        if len(dictstack) < 1:
            dictPush()
        #add name:value pair to top dict
        dictstack[-1][0][name] = value
        return True
    else:
        return False

def lookup(name):
    """Return most recently defined value for name. None if not found.
    
       name should not have a leading '/'."""
    for x in reversed(dictstack):
        for key in x:
            if key == '/'+name:
                return x[key]
    else:
        print('error: name not found')

def dLookup(name):
    """Return most recently defined value for name. None if not found.
    
       name should not have a leading '/'."""
    for index, x in enumerate(reversed(dictstack)):
        for key in x[0]:
            if key == '/'+name:
                return (x[0][key], len(dictstack) - index - 1)
    else:
        print('error: name not found')
        return (None, None)

#lookup for assignment 5
def sLookup(name):
    #if dict stack is empty exit
    if len(dictstack) == 0:
        print('error: name not found')
        return (None, None)
    #look in dict at top of stack, follow static chain
    i = len(dictstack)-1
    while True:
        for key in dictstack[i][0]:
            if key == '/'+name:
                return(dictstack[i][0][key], i)
        #if end of chain and value not found, break
        if i == dictstack[i][1]:
            break;
        #go to next link in chain
        i = dictstack[i][1]

    print('error: name not found')
    return (None, None)


#Arithmetic and comparison operators
    """Pop opstack twice and push sum."""
    opBase(lambda x:x[1]+x[0], isNumeric)

def sub():
    """Pop opstack twice and push difference."""
    opBase(lambda x:x[1]-x[0], isNumeric)

def mul():
    """Pop opstack twice and push product."""
    opBase(lambda x:x[1]*x[0], isNumeric)

def div():
    """Pop opstack twice and push quotient."""
    opBase(lambda x:x[1]/x[0], isNumeric)

def mod():
    """Pop opstack twice and push remainder."""
    opBase(lambda x:x[1]%x[0], isNumeric)

def lt():
    """Pop opstack twice and push result of op1<op2."""
    opBase(lambda x:x[1]<x[0], isNumeric)

def gt():
    """Pop opstack twice and push result of op1>op2."""
    opBase(lambda x:x[1]>x[0], isNumeric)

def eq():
    """Pop opstack twice and push result of op1==op2."""
    opBase(lambda x:x[1]==x[0], isNumeric)

def neg():
    """Pop opstack and push negation onto opstack."""
    opBase(lambda x:-x[0], isNumeric, 1)

#array operators
def put():
    """Pop value, index, and array, push array[index] = val."""
    def operation(ops):
        val, index, arr = ops
        arr[index] = val
        return arr

    def typeCheck(ops):
        tests = []
        arr, index, val = ops
        tests.append(isinstance(index, int))
        tests.append(isinstance(arr, list))
        return all(tests)

    opBase(operation, typeCheck, 3) 

def length():
    """Pop array from stack and push length of array."""
    opBase(lambda x:len(x[0]), lambda x:isinstance(x[0], list), 1)

def get():
    """Pop index and array from opstack and push val array[index]."""
    def typeCheck(ops):
        tests = []
        arr, index = ops
        tests.append(isinstance(arr, list))
        tests.append(isinstance(index, int))
        return all(tests)

    opBase(lambda x:x[1][x[0]], typeCheck)

#boolean operators
def isBool(args):
    """Return true if all values in args are numeric."""
    for x in args:
        if not isinstance(x, bool):
            return False
    else:
        return True

def psAnd():
    """Pop opstack twice and push result of op1 AND op2."""
    opBase(lambda x:x[0] and x[1], isBool)

def psOr():
    """Pop opstack twice and push result of op1 OR op2."""
    opBase(lambda x:x[0] or x[1], isBool)

def psNot():
    """Pop opstack and push result of NOT."""
    opBase(lambda x:not x[0], isBool, 1)

#stack manipulation and operators
def dup():
    opBase(lambda x: [x[0], x[0]], nops=1)

def exch():
    """Exchange top two opstack values."""
    opBase(lambda x:x)

def pop():
    """Pop opstack and return value."""
    return opPop()

def copy():
    """Pop opstack and copy the top op1 values onto opstack."""
    def operation(ops):
        push = list(ops[1:])
        push.extend(push)
        return reversed(push)

    opBase(operation, nops=opstack[-1]+1)

def clear():
    """Clear all items from opstack."""
    opstack.clear()

def stack():
    """Diplay contents of opstack."""
    print(gscope)
    print('==============')
    for x in reversed(opstack):
        print(x)
    print('==============')

    #print dict stack
    for index, x in enumerate(reversed(dictstack)):
        print('----', len(dictstack) - index - 1, '----', x[1], '----', sep='')
        for key in x[0]:
            print(key, '   ', x[0][key])
    print('==============')

def popPrint():
    print(pop())

def count():
    opPush(len(opstack))

#dictionary manipulation operators
def psDict():
    """Pop integer off opstack and push an empty dict."""
    #pop integer off stack
    opBase(lambda x:(), isNumeric, 1)
    opPush({})

def begin():
    """Pop dict from opstack and push onto dictstack."""
    if len(opstack) > 0 and isinstance(opstack[-1], dict):
        dictPush(opPop())

def end():
    """Pop dictstack."""
    dictstack.pop()

def psDef():
    """Pop a value then name off opstack and add definition."""
    def operation(ops):
        val, name = ops
        define(name, val)
        return ()

    opBase(operation, nops=2)

#-------------------------Part 2----------------------------------------

#control operators
def psIf():
    """Pop a bool and code block from opstack, exe code if bool is true."""
    def operator(ops):
        if ops[1]:
            interpretSPS(ops[0], gscope)
    def typecheck(ops):
        return isinstance(ops[1], list) and not all(isinstance(x, int) for x in ops[1]) and isinstance(ops[0], bool)

    opBase(operator, typecheck)
    #pop result of operator off of stack since no result is desired
    opPop()

def psIfelse():
    """pop a bool and two codeblocks from opstack, exe first block if bool is
    true, second block if false."""
    def operator(ops):
        if ops[2]:
            interpretSPS(ops[1], gscope)
        else:
            interpretSPS(ops[0], gscope)

    def typecheck(ops):
        return isinstance(ops[2], list) and isinstance(ops[1], list) and isinstance(ops[0], bool)

    opBase(operator, typecheck, 3)
    #pop result of operator off of stack since no result is desired
    opPop()

def psFor():
    """Pop <init><incr><final><codearray> off opstack, pushing the current
    iteration value to opstack then executing the codearray for each loop."""
    def operator(ops):
        #unpack ops for clarity
        code_array, final, incr, init = ops
        #make range inclusive
        if incr > 0:
            end = final + 1
        else:
            end = final - 1
        for x in range(init, end, incr):
            opPush(x)
            #print('after push: ', t.opstack)
            interpretSPS(code_array, gscope)
            #print('after eval: ', t.opstack)

    def typecheck(ops):
        #unpack ops for clarity
        init, incr, final, code_array = ops
        tests = []
        tests.append(isinstance(init, int))
        tests.append(isinstance(incr, int))
        tests.append(isinstance(final, int))
        tests.append(isinstance(code_array, list) and
            not all(isinstance(x, int) for x in code_array))
        return all(tests)
    
    opBase(operator, typecheck, 4)
    #pop result of operator off of stack since no result is desired
    opPop()

def forAll():
    """Pop array and codeblock from opstack, execute codeblock on each item in
    array pushing each result to opstack."""
    def operator(ops):
        #unpack ops for clarity
        procedure, arr = ops
        for x in arr:
            opPush(x)
            interpretSPS(procedure, gscope)

    def typecheck(ops):
        #unpack ops for clarity
        arr, procedure = ops
        tests = []
        tests.append(isinstance(arr, list) and all(isinstance(x, int) for x
            in arr))
        tests.append(isinstance(procedure, list) and
            not all(isinstance(x, int) for x in procedure))
        return all(tests)

    opBase(operator, typecheck)
    #pop result of operator off stack since no result is desird
    opPop()
        

#tokenizes an input string
def tokenize(s):
    """Break an input string into list of tokens."""
    return re.findall("/?[a-zA-Z][a-zA-Z0-9_]*|[[][a-zA-Z0-9_\s!][a-zA-Z0\
        -9_\s!]*[]]|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)

#matches code arrays
def groupMatching2(it):
    """Creates sublists of matching '{' characters."""
    res = []
    for c in it:
        if c == '}':
            return res
        elif c == '{':
            res.append(groupMatching2(it))
        else:
            res.append(convert(c))
    return False

#tokenize an integer array
def tokenizeArray(s):
    """Break an array string into tokens."""
    return re.findall('\[|\]|\d[0-9.]*', s)

#matches integer arrays
def groupMatching3(it):
    """Creates sublists of matching '[' characters."""
    res = []
    for c in it:
        if c == ']':
            return res
        elif c == '[':
            res.append(groupMatching3(it))
        else:
            res.append(convert(c))
    return res

#converts tokens to the correct python data type
def convert(c):
    """Converts a string into the corresponding python data type."""
    #integer
    if c.isdigit() or (c[0] == '-' and c[1:].isdigit):
        return int(c)
    #float
    if c.replace('.','',1).isdigit():
        return float(c)
    #boolean
    elif c == 'true':
        return(True)
    elif c == 'false':
        return(False)
    #array
    elif c[0] == '[':
        #return index 0 to remove outer list
        return groupMatching3(iter(tokenizeArray(c)))[0]
    #named constant
    else:
        return c

#accepts list of tokens from tokenize, converting into correct python types
def parse(tokens):
    """Converts a list of input tokens into python data types for use."""
    res = []
    it = iter(tokens)
    for c in it:
        if c == '}':
            return False
        elif c == '{':
            res.append(groupMatching2(it))
        else:
            res.append(convert(c))
    return res

#interprets code arrays
def interpretSPS(code, scope):
    """Executes code arrays created with parse()."""
    operators = {'add':add, 'sub':sub, 'mul':mul, 'div':div, 'mod':mod,
    'lt':lt, 'gt':gt, 'eq':eq, 'neg':neg, 'put':put, 'length':length,
    'get':get, 'and':psAnd, 'or':psOr, 'not':psNot, 'dup':dup, 'exch':exch,
    'pop':pop, 'copy':copy, 'clear':clear, 'stack':stack, '=':popPrint,
    'count':count, 'def':psDef, 'if':psIf, 'ifelse':psIfelse, 'for':psFor,
    'forall':forAll}

    #set gscope for branch operators
    global gscope
    gscope = scope

    #handle each value
    for value in code:
        #value
        if isinstance(value, (int, float, list)):
            opPush(value)
        #operator
        elif value in operators:
            operators[value]()
        #name constant
        elif isinstance(value, str) and value[0] == '/':
            opPush(value)
        #variable
        elif isinstance(value, str):
            #dynamic scoping
            if scope == 'dynamic':
                lookupVal, slink = dLookup(value)
            #static scoping
            elif scope == 'static':
                lookupVal, slink = sLookup(value)
            #check variable exists
            if lookupVal:
                #codeblock
                if isinstance(lookupVal, list) and not all(isinstance(x, int)
                    for x in lookupVal):
                    #push new dict
                    dictPush({}, slink)
                    interpretSPS(lookupVal, scope)
                    #pop dict
                    dictPop();
                #value
                else:
                    opPush(lookupVal)
        else:
            print('invalid input')

def interpreter(s, scope):
    """Calls necessary functions to execute an SPS input string."""
    if scope != 'static' and scope != 'dynamic':
        print('invalid scope')
    else:
        interpretSPS(parse(tokenize(s)), scope)

#-------------------------TEST FUNCTIONS--------------------------------

import re
#global variables
opstack = []  #assuming top of the stack is the end of the list
dictstack = []  #assuming top of the stack is the end of the list


#------- Part 1 TEST CASES--------------
#Test cases provided by Sakire and Reid Reininger.
def testDefine():
    define("/n1", 4)
    if lookup("n1") != 4:
        return False
    return True

def testDefine2():
    define("/n2", [1,2,3])
    if lookup("n2") != [1,2,3]:
        return False
    return True

def testDefine3():
    define("/n3", "test string")
    if lookup("n3") != "test string":
        return False
    return True

def testDefine4():
    return not define("n4", 5)

def testDefine5():
    return not define("/4", 6)

def testLookup():
    opPush("/n1")
    opPush(3)
    psDef()
    if lookup("n1") != 3:
        return False
    return True

def testLookup2():
    opPush("/n2")
    opPush(-1)
    psDef()
    if lookup("n2") != -1:
        return False
    return True

def testLookup3():
    opPush("/n3")
    opPush("test")
    psDef()
    if lookup("n3") != "test":
        return False
    return True

#Arithmatic operator tests
def testAdd():
    opPush(1)
    opPush(2)
    add()
    if opPop() != 3:
        return False
    return True

def testAdd2():
    opPush(4.5)
    opPush(2.5)
    add()
    if opPop() != 7:
        return False
    return True

def testSub():
    opPush(10)
    opPush(4.5)
    sub()
    if opPop() != 5.5:
        return False
    return True

def testSub2():
    opPush(9)
    opPush(14)
    sub()
    if opPop() != -5:
        return False
    return True

def testMul():
    opPush(2)
    opPush(4.5)
    mul()
    if opPop() != 9:
        return False
    return True

def testMul2():
    opPush(-3)
    opPush(6)
    mul()
    if opPop() != -18:
        return False
    return True

def testDiv():
    opPush(10)
    opPush(4)
    div()
    if opPop() != 2.5:
        return False
    return True

def testDiv2():
    opPush(-6)
    opPush(2)
    div()
    if opPop() != -3:
        return False
    return True
    
    
#Comparison operators tests
def testEq():
    opPush(6)
    opPush(6)
    eq()
    if opPop() != True:
        return False
    return True

def testEq2():
    opPush(7)
    opPush(6)
    eq()
    if opPop() != False:
        return False
    return True

def testLt():
    opPush(3)
    opPush(6)
    lt()
    if opPop() != True:
        return False
    return True

def testLt2():
    opPush(6)
    opPush(3)
    lt()
    if opPop() != False:
        return False
    return True

def testGt():
    opPush(3)
    opPush(6)
    gt()
    if opPop() != False:
        return False
    return True

def testGt2():
    opPush(6)
    opPush(2)
    gt()
    if opPop() != True:
        return False
    return True

#boolean operator tests
def testPsAnd():
    opPush(True)
    opPush(False)
    psAnd()
    if opPop() != False:
        return False
    return True

#boolean operator tests
def testPsAnd2():
    opPush(True)
    opPush(True)
    psAnd()
    if opPop() != True:
        return False
    return True

def testPsOr():
    opPush(True)
    opPush(False)
    psOr()
    if opPop() != True:
        return False
    return True

def testPsOr2():
    opPush(False)
    opPush(False)
    psOr()
    if opPop() != False:
        return False
    return True

def testPsNot():
    opPush(True)
    psNot()
    if opPop() != False:
        return False
    return True

def testPsNot2():
    opPush(False)
    psNot()
    if opPop() != True:
        return False
    return True

#Array operator tests
def testLength():
    opPush([1,2,3,4,5])
    length()
    if opPop() != 5:
        return False
    return True

def testLength2():
    opPush([])
    length()
    if opPop() != 0:
        return False
    return True

def testGet():
    opPush([1,2,3,4,5])
    opPush(4)
    get()
    if opPop() != 5:
        return False
    return True

def testGet2():
    opPush([1,2,3,4,5])
    opPush(0)
    get()
    if opPop() != 1:
        return False
    return True

#stack manipulation functions
def testDup():
    opPush(10)
    dup()
    if opPop()!=opPop():
        return False
    return True

def testDup2():
    opPush('test')
    dup()
    if opPop()!=opPop():
        return False
    return True

def testExch():
    opPush(-5)
    opPush("/x")
    exch()
    if opPop()!=10 and opPop()!="/x":
        return False
    return True

def testPop():
    l1 = len(opstack)
    opPush(-5)
    pop()
    l2= len(opstack)
    if l1!=l2:
        return False
    return True

def testCopy():
    opPush(1)
    opPush(2)
    opPush(3)
    opPush(4)
    opPush(5)
    opPush(2)
    copy()
    if opPop()!=5 and opPop()!=4 and opPop()!=5 and opPop()!=4 and opPop()!=3 and opPop()!=2:
        return False
    return True

def testClear():
    opPush(10)
    opPush("/x")
    clear()
    if len(opstack)!=0:
        return False
    return True

#dictionary stack operators
def testDict():
    opPush(1)
    psDict()
    if opPop()!={}:
        return False
    return True

def testBeginEnd():
    opPush("/x")
    opPush(3)
    psDef()
    opPush({})
    begin()
    opPush("/x")
    opPush(4)
    psDef()
    end()
    if lookup("x")!=3:
        return False
    return True

def testpsDef():
    opPush("/x")
    opPush(10)
    psDef()
    if lookup("x")!=10:
        return False
    return True

def testpsDef2():
    opPush("/x")
    opPush(10)
    psDef()
    opPush(1)
    psDict()
    begin()
    if lookup("x")!=10:
        end()
        return False
    end()
    return True

#------------------PART2 TEST CASES----------------------------
def testpsIf():
    global opstack
    opstack = [True, [3, 1, 'add']]
    psIf()
    if opstack[0] == 4:
        return True
    return False

def testpsIf2():
    global opstack
    opstack = [False, [3, 1, 'add']]
    psIf()
    if opstack == []:
        return True
    return False

def testpsIfelse():
    global opstack
    opstack = [True, [3, 1, 'add'], [3, 1, 'mul']]
    psIfelse()
    if opstack[0] == 4:
        return True
    return False

def testpsIfelse2():    
    global opstack
    opstack = [False, [3,1,'add'], [3,1,'mul']]
    psIfelse()
    if opstack[0] == 3:
        return True
    return False

def testpsFor():
    global opstack
    opstack = [1,1,3,[10, 'mul']]
    psFor()
    if opstack == [10, 20, 30]:
        return True
    return False

def testpsFor2():
    global opstack
    opstack = [1,1,5,['dup']]
    psFor()
    if opstack == [1,1,2,2,3,3,4,4,5,5]:
        return True
    return False

def testforAll():
    global opstack
    opstack = [[1,2,3,4], [2, 'mul']]
    forAll()
    return opstack == [2,4,6,8]

def testforAll2():
    global opstack
    opstack = [[1,2,3,4], [2, 'add']]
    forAll()
    return opstack == [3,4,5,6]

#inputs for tokenize and parse testing
input1 = """
    /square {dup mul} def
    [1 2 3 4] {square} forall
    add add add 30 eq true
    stack
"""

input2 = """
    [1 2 3 4 5] dup length /n exch def
    /fact {
        0 dict begin
            /n exch def
            n 2 lt
            { 1}
            {n 1 sub fact n mul }
            ifelse
        end
    } def
    n fact stack
"""

input3 = """
    [9 9 8 4 10] {dup 5 lt {pop} if} forall
    stack
"""

input4 = """
    [1 2 3 4 5] dup length exch {dup mul}    forall
    add add add add
    exch 0 exch -1 1 {dup mul add} for
    eq stack
"""

input5 = """
    /n 2 def
    0 dict begin
    /n 3 def
    n end n add
    stack
"""

input6 = """
    2 3 add
    4 sub
    10 mul
    2 div
    3 mod
    /square {dup mul} def
    square
    stack
"""

def testtokenize():
    return tokenize(input1) == ['/square', '{', 'dup', 'mul', '}', 'def',
        '[1 2 3 4]', '{', 'square', '}', 'forall', 'add', 'add', 'add', '30',
        'eq', 'true', 'stack']

def testtokenize2():
    return tokenize(input2) == ['[1 2 3 4 5]', 'dup', 'length', '/n', 'exch',
        'def', '/fact', '{', '0', 'dict', 'begin', '/n', 'exch', 'def', 'n',
        '2', 'lt', '{', '1', '}', '{', 'n', '1', 'sub', 'fact', 'n', 'mul',
        '}', 'ifelse', 'end', '}', 'def', 'n', 'fact', 'stack']

def testtokenize3():
    return tokenize(input3) == ['[9 9 8 4 10]', '{', 'dup', '5', 'lt', '{',
        'pop', '}', 'if', '}', 'forall', 'stack']

def testtokenize4():
    return tokenize(input4) == ['[1 2 3 4 5]', 'dup', 'length', 'exch', '{',
    'dup', 'mul', '}', 'forall', 'add', 'add', 'add', 'add', 'exch', '0',
    'exch', '-1', '1', '{', 'dup', 'mul', 'add', '}', 'for', 'eq', 'stack']

def testparse():
    return parse(tokenize(input1)) == ['/square', ['dup', 'mul'], 'def', [1, 2,
    3,4], ['square'], 'forall', 'add', 'add', 'add', 30, 'eq', True, 'stack']

def testparse2():
    return parse(tokenize(input2)) == [[1,2,3,4,5], 'dup', 'length', '/n',
    'exch', 'def', '/fact', [0, 'dict', 'begin', '/n', 'exch', 'def', 'n', 2,
    'lt', [1], ['n', 1, 'sub', 'fact', 'n', 'mul'], 'ifelse', 'end'], 'def',
    'n', 'fact', 'stack']

def testparse3():
    return parse(tokenize(input3)) == [[9, 9, 8, 4,10], ['dup', 5, 'lt',
    ['pop'], 'if'], 'forall', 'stack']

def testparse4():
    return parse(tokenize(input4)) == [[1,2,3,4,5], 'dup', 'length', 'exch',
    ['dup', 'mul'], 'forall', 'add', 'add', 'add', 'add', 'exch', 0, 'exch',
    -1, 1, ['dup', 'mul', 'add'], 'for', 'eq', 'stack']

def testtokenizeArray():
    return tokenizeArray('[1 2 3 4]') == ['[', '1', '2', '3', '4', ']']

def testtokenizeArray2():
    return tokenizeArray('[1 2 [3 4] 5]') == ['[', '1', '2', '[', '3', '4', ']',
    '5', ']']

def testconvert():
    #integer
    return convert('1') == 1

def testconvert2():
    #float
    return convert('1.0') == 1.0

def testconvert3():
    #boolean
    return convert('true') == True

def testconvert4():
    #boolean
    return convert('false') == False

def testconvert5():
    #array
    return convert('[1 2 3]') == [1,2,3]

def testconvert6():
    #named constant
    return convert('/lol') == '/lol'

def testinterpreter():
    global opstack
    global dictstack
    opstack.clear()
    dictstack.clear()
    print('interpreter input1 test:')
    interpreter(input1)
    return opstack == [True, True] and dictstack == [{'/square': ['dup',
        'mul']}] 

def testinterpreter2():
    global opstack
    global dictstack
    opstack.clear()
    dictstack.clear()
    print('interpreter input2 test:')
    interpreter(input2)
    return opstack == [[1,2,3,4,5], 120] and dictstack == [{'/square': ['dup',
        'mul'], '/fact': [0, 'dict', 'begin', '/n', 'exch', 'def', 'n', 2, 'lt',
        [1], ['n', 1, 'sub', 'fact', 'n', 'mul'], 'ifelse', 'end'], '/n': 5}]

def testinterpreter3():
    global opstack
    global dictstack
    opstack.clear()
    dictstack.clear()
    print('interpreter input3 test:')
    interpreter(input3)
    return opstack == [9,9,8,10] and dictstack == []

def testinterpreter4():
    global opstack
    global dictstack
    dictstack.clear()
    opstack.clear()
    print('interpreter input4 test:')
    interpreter(input4)
    return opstack == [True] and dictstack == []

def testinterpreter5():
    global opstack
    global dictstack
    opstack.clear()
    dictstack.clear()
    print('interpreter input5 test:')
    interpreter('/n 2 def 0 dict begin /n 3 def n end n add stack')
    return opstack == [5] and dictstack == [{'/square': ['dup', 'mul'],
        '/fact': [0, 'dict', 'begin', '/n', 'exch', 'def', 'n', 2, 'lt', [1], ['n',
        1, 'sub', 'fact', 'n', 'mul'], 'ifelse', 'end'], '/n': 2}]

def testinterpreter6():
    global opstack
    global dictstack
    opstack.clear()
    dictstack.clear()
    print('interpreter input6 test:')
    interpreter(input6)
    return opstack == [4.0] #and dictstack == [{'/square': ['dup', 'mul']}]

#------------------Part 3 test cases---------------------------
sspsInput1 = """
/x 4 def /g { x stack } def /f { /x 7 def g } def f
"""
sspsInput2 = """
/m 50 def /n 100 def /egg1 {/m 25 def n} def /chic {     /n 1 def     /egg2 { n
} def     m  n     egg1     egg2     stack  } def n chic
"""
sspsInput3 = """
/x 10 def /A { x } def /C { /x 40 def A stack } def /B { /x 30 def /A { x } def
C } def B
"""
sspsInput4 = """
    2 3 add
    4 sub
    10 mul
    2 div
    3 mod
    /square {dup mul} def
    square
    stack
"""
sspsInput5 = """
    2 3 add
    4 sub
    10 mul
    2 div
    3 mod
    /square {dup mul} def
    square
    stack
"""


def testSSPS():
    global opstack
    global dictstack
    opstack.clear()
    dictstack.clear()
    print('SSPS input1 static test:')
    interpreter(sspsInput1, 'static')
    return opstack == [4] and dictstack == [({'/g': ['x', 'stack'], '/x': 4,
    '/f': ['/x', 7, 'def', 'g']}, 0)]

def testSSPS1():
    global opstack
    global dictstack
    opstack.clear()
    dictstack.clear()
    print('SSPS input1 dynamic test:')
    interpreter(sspsInput1, 'dynamic')
    return opstack == [7] and dictstack == [({'/g': ['x', 'stack'], '/x': 4,
    '/f': ['/x', 7, 'def', 'g']}, 0)]


def testSSPS2():
    global opstack
    global dictstack
    opstack.clear()
    dictstack.clear()
    print('SSPS input2 static test:')
    interpreter(sspsInput2, 'static')
    return opstack == [100, 50, 1, 100, 1] and dictstack == [({'/chic': ['/n',
    1, 'def', '/egg2', ['n'], 'def', 'm', 'n', 'egg1', 'egg2', 'stack'], '/n':
    100, '/m': 50, '/egg1': ['/m', 25, 'def', 'n']}, 0)]

def testSSPS3():
    global opstack
    global dictstack
    opstack.clear()
    dictstack.clear()
    print('SSPS input2 dynamic test:')
    interpreter(sspsInput2, 'dynamic')
    return opstack == [1, 1, 1, 50, 100] and dictstack == [({'/chic': ['/n',
    1, 'def', '/egg2', ['n'], 'def', 'm', 'n', 'egg1', 'egg2', 'stack'], '/n':
    100, '/m': 50, '/egg1': ['/m', 25, 'def', 'n']}, 0)]

def testSSPS4():
    global opstack
    global dictstack
    opstack.clear()
    dictstack.clear()
    print('SSPS input3 static test:')
    interpreter(sspsInput3, 'static')
    return opstack == [10] and dictstack == [({'/B': ['/x', 30, 'def', '/A',
    ['x'], 'def', 'C'], '/A': ['x'], '/C': ['/x', 40, 'def', 'A', 'stack'],
    '/x': 10}, 0)]

def testSSPS5():
    global opstack
    global dictstack
    opstack.clear()
    dictstack.clear()
    print('SSPS input3 dynamic test:')
    interpreter(sspsInput3, 'dynamic')
    return opstack == [40] and dictstack == [({'/B': ['/x', 30, 'def', '/A',
    ['x'], 'def', 'C'], '/A': ['x'], '/C': ['/x', 40, 'def', 'A', 'stack'],
    '/x': 10}, 0)]

def testSSPS6():
    global opstack
    global dictstack
    opstack.clear()
    dictstack.clear()
    print('SSPS input4 static test:')
    interpreter(sspsInput4, 'static')
    return opstack == [4.0] and dictstack == [({'/square': ['dup', 'mul']}, 0)]

def testSSPS7():
    global opstack
    global dictstack
    opstack.clear()
    dictstack.clear()
    print('SSPS input4 dynamic test:')
    interpreter(sspsInput4, 'dynamic')
    return opstack == [4.0] and dictstack == [({'/square': ['dup', 'mul']}, 0)]

def testSSPS8():
    global opstack
    global dictstack
    opstack.clear()
    dictstack.clear()
    print('SSPS input5 static test:')
    interpreter(sspsInput5, 'static')
    return opstack == [4.0] and dictstack == [({'/square': ['dup', 'mul']},
	0)]

def testSSPS9():
    global opstack
    global dictstack
    opstack.clear()
    dictstack.clear()
    print('SSPS input5 dynamic test:')
    interpreter(sspsInput5, 'dynamic')
    return opstack == [4.0] and dictstack == [({'/square': ['dup', 'mul']},
	0)]

#------------------RUN TESTS-----------------------------------

def main_part1():
    testCases = [
        ('define',testDefine),
        ('define2', testDefine2),
        ('define3', testDefine3),
        ('define4', testDefine4),
        ('define5', testDefine5),
        ('lookup',testLookup),
        ('lookup2',testLookup2),
        ('lookup3',testLookup3),
        ('add', testAdd),
        ('add2', testAdd2),
        ('sub', testSub),
        ('sub2', testSub2),
        ('mul', testMul),
        ('mul2', testMul2),
        ('div', testDiv),
        ('div2', testDiv2),
        ('eq',testEq),
        ('eq2',testEq2),
        ('lt',testLt),
        ('lt2',testLt2),
        ('gt', testGt),
        ('gt2', testGt2),
        ('psAnd', testPsAnd),
        ('psAnd2', testPsAnd2),
        ('psOr', testPsOr),
        ('psOr2', testPsOr2),
        ('psNot', testPsNot),
        ('psNot2', testPsNot2),
        ('length', testLength),
        ('length2', testLength2),
        ('get', testGet),
        ('get2', testGet2),
        ('dup', testDup),
        ('dup2', testDup2),
        ('exch', testExch),
        ('pop', testPop),
        ('copy', testCopy),
        ('clear', testClear),
        ('dict', testDict),
        ('begin', testBeginEnd),
        ('psDef', testpsDef),
        ('psDef2', testpsDef2)
    ]
    # add you test functions to this list along with suitable names
    failedTests = [testName for (testName, testProc) in testCases if not testProc()]
    #clear stacks
    global opstack
    global dictstack
    opstack.clear()
    dictstack.clear()
    
    if failedTests:
        return ('Some tests failed', failedTests)
    else:
        return ('All part-1 tests OK')

def main_part2():
    testCases = [
        ('psIf', testpsIf),
        ('psIf2', testpsIf2),
        ('psIfelse', testpsIfelse),
        ('psIfelse2', testpsIfelse2),
        ('psFor', testpsFor),
        ('psFor2', testpsFor2),
        ('psforAll', testforAll),
        ('psforAll2', testforAll2),
        ('tokenize', testtokenize),
        ('tokenize2', testtokenize2),
        ('tokenize3', testtokenize3),
        ('tokenize4', testtokenize4),
        ('parse', testparse),
        ('parse2', testparse2),
        ('parse3', testparse3),
        ('parse4', testparse4),
        ('tokenizeArray', testtokenizeArray),
        ('tokenizeArray2', testtokenizeArray2),
        ('convert', testconvert),
        ('convert2', testconvert2),
        ('convert3', testconvert3),
        ('convert4', testconvert4),
        ('convert5', testconvert5),
        ('convert6', testconvert6),
        ('interpreter', testinterpreter),
        ('interpreter2', testinterpreter2),
        ('interpreter3', testinterpreter3),
        ('interpreter4', testinterpreter4),
        ('interpreter5', testinterpreter5),
        ('interpreter6', testinterpreter6)
    ]
    # add you test functions to this list along with suitable names
    failedTests = [testName for (testName, testProc) in testCases if not testProc()]

    #clear stacks
    global opstack
    global dictstack
    opstack.clear()
    dictstack.clear()


    
    if failedTests:
        return ('Some tests failed', failedTests)
    else:
        return ('All part-2 tests OK')

def main_hw5():
    testCases = [
        ('testSSPS dynamic input 1', testSSPS),
        ('testSSPS static input 1', testSSPS1),
        ('testSSPS dynamic input 2', testSSPS2),
        ('testSSPS static input 2', testSSPS3),
        ('testSSPS dynamic input 3', testSSPS4),
        ('testSSPS static input 3', testSSPS5),
        ('testSSPS dynamic input 4', testSSPS6),
        ('testSSPS static input 4', testSSPS7),
        ('testSSPS dynamic input 5', testSSPS8),
        ('testSSPS static input 5', testSSPS9),
    ]
    # add you test functions to this list along with suitable names
    failedTests = [testName for (testName, testProc) in testCases if not testProc()]

    #clear stacks
    opstack.clear()
    dictstack.clear()
    
    if failedTests:
        return ('Some tests failed', failedTests)
    else:
        return ('All part-2 tests OK')

if __name__ == '__main__':
    #print(main_part2())
    #print(main_part1())
    #print(main_hw5())
