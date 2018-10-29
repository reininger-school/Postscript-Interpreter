#programmer: Reid Reininger(charles.reininger@wsu.edu)
#date: 10/24/18
#desc: Intended for Unix/Systems. Interpretor for Postscript.

#used to check if data is numeric for arithmetic operators
from numbers import Number

#to check for iterable object types
from collections.abc import Iterable

#globals
opstack = []
dictstack = [{}]

#operand stack operators
def opPop():
    """Pop opstack and return None on failure."""
    if len(opstack) >= 1:
        return opstack.pop()
    else:
        print('error: not enough items in opstack')

def opPush(value):
    """Push value onto opstack."""
    return opstack.append(value)

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

def dictPush():
    """Push empty dict onto dictstack."""
    return dictstack.append({})

def define(name, value):
    """Add name:value pair to top dict in dictstack. Return True on
       success."""
    if len(dictstack) > 0:
        dictstack[-1][name] = value
        return True
    else:
        print('error: dictstack is empty')
        return False

def lookup(name):
    """Return most recently defined value for name. None if not found."""
    for x in reversed(dictstack):
        for key in x:
            if key == name:
                return x[key]
    else:
        print('error: name not found')

def begin():
    if len(opstack) > 0 and isinstance(opstack[-1], dict):
        dictPush(opPop())


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
    opBase(lambda x:x[0]+x[1], isNumeric)

def sub():
    """Pop opstack twice and push difference."""
    opBase(lambda x:x[0]-x[1], isNumeric)

def mul():
    """Pop opstack twice and push product."""
    opBase(lambda x:x[0]*x[1], isNumeric)

def mod():
    """Pop opstack twice and push remainder."""
    opBase(lambda x:x[0]%x[1], isNumeric)

def lt():
    """Pop opstack twice and push result of op1<op2."""
    opBase(lambda x:x[0]<x[1], isNumeric)

def gt():
    """Pop opstack twice and push result of op1>op2."""
    opBase(lambda x:x[0]>x[1], isNumeric)

def eq():
    """Pop opstack twice and push result of op1==op2."""
    opBase(lambda x:x[0]==x[1], isNumeric)

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
