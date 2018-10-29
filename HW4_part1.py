#programmer: Reid Reininger(charles.reininger@wsu.edu)
#date: 10/24/18
#desc: Intended for Unix/Linux Systems. Interpreter for Simplified
#       Postscript(SPS).

#used to check if data is numeric for arithmetic operators
from numbers import Number

#to check for iterable object types
from collections.abc import Iterable

#globals
opstack = []
dictstack = []

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

def dictPush(dictionary={}):
    """Push empty dict onto dictstack by default and return False on failure."""
    if isinstance(dictionary, dict):
        dictstack.append(dictionary)
        return True
    else:
        print('error: only dictionaries may be pushed to dictstack')
        return False

def define(name, value):
    """Add name:value pair to top dict in dictstack and return False on fail."""

    def isValidName(string):
        """Return true if string is a valid name."""
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
        dictstack[-1][name] = value
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


#Arithmetic and comparison operators
def opBase(operator, typeCheck=lambda x:True, nops=2):
    """Base function for operand functions.

       Pop nops items off opstack, and push the result of operator. typeCheck
       is an optional boolean func to check the popped arguments."""
    if len(opstack) >= nops:
        if typeCheck(opstack[-nops:]):
            ops = opPopn(nops)
            results = operator(ops)
            if isinstance(results, Iterable):
                for x in results:
                    opPush(x)
            else:
                opPush(results)
        else:
            print('error: arguments of incorrect type')
    else:
        print('error: not enough arguments on opstack')

def isNumeric(args):
    """Return true if all values in args are numeric."""
    for x in args:
        if not isinstance(x, Number):
            return False
    else:
        return True

def add():
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
    def helper(ops):
        val, index, arr = ops
        arr[index] = val
        return arr

    opBase(helper, nops=3) 

def length():
    """Pop array from stack and push lenght of array."""
    opBase(lambda x:len(x[0]), nops=1)

def get():
    """Pop index and array from opstack and push val array[index]."""
    opBase(lambda x:x[1][x[0]])

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
    opBase(lambda x:not x[0], isBool, nops=1)

#stack manipulation operators
def dup():
    if len(opstack) > 0:
        opPush(opstack[-1])
    else:
        print('error: not enough arguments on opstack')

def exch():
    """Exchange top two opstack values."""
    opBase(lambda x:x, nops = 2)

def pop():
    """Pop opstack and return value."""
    return opPop()

def copy():
    """Pop opstack and copy the top op1 values onto opstack."""
    def helper(ops):
        push = list(ops[1:])
        push.extend(push)
        return reversed(push)

    opBase(helper, nops=opstack[-1]+1)

def clear():
    """Clear all items from opstack."""
    opstack.clear()

def stack():
    """Diplay contents of opstack."""
    for x in reversed(opstack):
        print(x)

#dictionary manipulation operators
def psDict():
    opBase(lambda x:(), isNumeric, 1)
    opPush({})

def begin():
    if len(opstack) > 0 and isinstance(opstack[-1], dict):
        dictPush(opPop())

def end():
    """Pop dictstack."""
    dictstack.pop()

def psDef():
    def helper(ops):
        val, name = ops
        define(name, val)
        return ()

    opBase(helper, nops=2)

#-------------------------TEST FUNCTIONS--------------------------------

import re
#global variables
opstack = []  #assuming top of the stack is the end of the list
dictstack = []  #assuming top of the stack is the end of the list


#------- Part 1 TEST CASES--------------
def testDefine():
    define("/n1", 4)
    if lookup("n1") != 4:
        return False
    return True

def testLookup():
    opPush("/n1")
    opPush(3)
    psDef()
    if lookup("n1") != 3:
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

def testSub():
    opPush(10)
    opPush(4.5)
    sub()
    if opPop() != 5.5:
        return False
    return True

def testMul():
    opPush(2)
    opPush(4.5)
    mul()
    if opPop() != 9:
        return False
    return True

def testDiv():
    opPush(10)
    opPush(4)
    div()
    if opPop() != 2.5:
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

def testLt():
    opPush(3)
    opPush(6)
    lt()
    if opPop() != True:
        return False
    return True

def testGt():
    opPush(3)
    opPush(6)
    gt()
    if opPop() != False:
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

def testPsOr():
    opPush(True)
    opPush(False)
    psOr()
    if opPop() != True:
        return False
    return True

def testPsNot():
    opPush(True)
    psNot()
    if opPop() != False:
        return False
    return True

#Array operator tests
def testLength():
    opPush([1,2,3,4,5])
    length()
    if opPop() != 5:
        return False
    return True

def testGet():
    opPush([1,2,3,4,5])
    opPush(4)
    get()
    if opPop() != 5:
        return False
    return True

#stack manipulation functions
def testDup():
    opPush(10)
    dup()
    if opPop()!=opPop():
        return False
    return True

def testExch():
    opPush(10)
    opPush("/x")
    exch()
    if opPop()!=10 and opPop()!="/x":
        return False
    return True

def testPop():
    l1 = len(opstack)
    opPush(10)
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


def main_part1():
    testCases = [('define',testDefine),('lookup',testLookup),('add', testAdd), ('sub', testSub),('mul', testMul),('div', testDiv), \
                 ('eq',testEq),('lt',testLt),('gt', testGt), ('psAnd', testPsAnd),('psOr', testPsOr),('psNot', testPsNot), \
                 ('length', testLength),('get', testGet), ('dup', testDup), ('exch', testExch), ('pop', testPop), ('copy', testCopy), \
                 ('clear', testClear), ('dict', testDict), ('begin', testBeginEnd), ('psDef', testpsDef), ('psDef2', testpsDef2)]
    # add you test functions to this list along with suitable names
    failedTests = [testName for (testName, testProc) in testCases if not testProc()]
    if failedTests:
        return ('Some tests failed', failedTests)
    else:
        return ('All part-1 tests OK')

if __name__ == '__main__':
    print(main_part1())
