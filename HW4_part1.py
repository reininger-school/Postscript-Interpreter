#programmer: Reid Reininger(charles.reininger@wsu.edu)
#date: 10/24/18
#desc: Intended for Unix/Systems. Interpretor for Postscript.

#used to check if data is numeric for arithmetic operators
from numbers import Number

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
            opPush(operator(ops))
        else:
            print('error: arguments must be numeric')
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

#boolean operators
def psAnd():
    """Pop opstack twice and push result of op1 AND op2."""
    opBase(lambda x:x[0] and x[1])

def psOr():
    """Pop opstack twice and push result of op1 OR op2."""
    opBase(lambda x:x[0] or x[1])

def psNot():
    """Pop opstack and push result of NOT."""
    opBase(lambda x:not x[0], nops=1)

