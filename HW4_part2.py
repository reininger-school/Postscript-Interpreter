#programmer: Reid Reininger(charles.reininger@wsu.edu)
#date: 10/24/18
#desc: Intended for Unix/Linux Systems. Interpreter for Simplified
#      Postscript(SPS).

#to check for iterable object types
from collections.abc import Iterable
import re

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

       Pop nops items off opstack, and push the result of operator. If result
       is iterable it is iterated over pushing each item to opstack, otherwise
       result is just pushed. typeCheck is an optional boolean func accepting
       tuple of args in popped order to check the popped arguments."""

    #check operation is valid
    tests = []
    tests.append(len(opstack) >= nops) #check enough items on stack
    tests.append(typeCheck(opstack[-nops:])) #type check args

    #exe operation
    if all(tests):
        ops = opPopn(nops)
        results = operator(ops)
        if isinstance(results, Iterable):
            for x in results:
                opPush(x)
        else:
            opPush(results)
    else:
        if not tests[0]:
            print('error: not enough arguments on opstack')
        if not tests[1]:
            print('error: arguments of incorrect type')

def isNumeric(args):
    """Return true if all values in args are numeric."""
    for x in args:
        if not isinstance(x, (int, float)):
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
    for x in reversed(opstack):
        print(x)

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
#tokenizes an input string
def tokenize(s):
    return re.findall("/?[a-zA-Z][a-zA-Z0-9_]*|[[][a-zA-Z0-9_\s!][a-zA-Z0\
        -9_\s!]*[]]|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)

#matches code arrays
def groupMatching2(it):
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
	return re.findall('\[|\]|\d[0-9]*', s)

#matches integer arrays
def groupMatching3(it):
	res = []
	for c in it:
		if c == ']':
			return res
		elif c == '[':
			res.append(groupMatching3(it))
		else:
			res.append(int(c))
	return res

#converts tokens to the correct python data type
def convert(c):
	#digit
	if c.isdigit():
		return int(c)
	#boolean
	elif c == 'true':
		return(True)
	elif c == 'false':
		return(False)
	#array
	elif c[0] == '[':
		#return index 0 to remove outer list
		return groupMatching3(iter(tokenizeArray(c)))[0]
	#string
	else:
		return c

#accepts list of tokens from tokenize, converting into correct python types
def parse(tokens):
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
def interpretSPS(code):
	pass

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
    if failedTests:
        return ('Some tests failed', failedTests)
    else:
        return ('All part-1 tests OK')

if __name__ == '__main__':
    print(main_part1())
