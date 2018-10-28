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


#Arithmetic and comparison operators
def binaryOpBase(operator, typeCheck=lambda x:True):
    """Pop opstack twice and push result of binary lambda operator.
    
       typeCheck is an optional boolean function to validate args."""
    if len(opstack) >= 2:
        if typeCheck(opstack[-2:]):
            op2, op1 = opPopn(2)
            opPush(operator(op1, op2))
        else:
            print('error: arguments must be numeric')
    else:
        print('error: not enough arguments on opstack')

def unaryOpBase(operator, typeCheck=lambda x:True):
    """Pop opstack and push result of unary lambda operator.
    
       typeCheck is an optional boolean function to validate args."""
    if len(opstack) >= 1:
        if typeCheck([opstack[-1]]):
            opPush(operator(opPop()))
        else: print('error: argument must be numeric')
    else: print('error: not enough arguments on opstack')

def isNumeric(args):
    """Return true if all values in args are numeric."""
    for x in args:
        if not isinstance(x, Number):
            return False
    else:
        return True

def add():
    """Pop opstack twice and push sum."""
    binaryOpBase(lambda x,y:x+y, isNumeric)

def sub():
    """Pop opstack twice and push difference."""
    binaryOpBase(lambda x,y:x-y, isNumeric)

def mul():
    """Pop opstack twice and push product."""
    binaryOpBase(lambda x,y:x*y, isNumeric)

def mod():
    """Pop opstack twice and push remainder."""
    binaryOpBase(lambda x,y:x%y, isNumeric)

def lt():
    """Pop opstack twice and push result of op1<op2."""
    binaryOpBase(lambda x,y:x<y, isNumeric)

def gt():
    """Pop opstack twice and push result of op1>op2."""
    binaryOpBase(lambda x,y:x>y, isNumeric)

def eq():
    """Pop opstack twice and push result of op1==op2."""
    binaryOpBase(lambda x,y:x==y, isNumeric)

def neg():
    """Pop opstack and push negation onto opstack."""
    unaryOpBase(lambda x:-x, isNumeric)

#array operators

#boolean operators
def psAnd():
    binaryOpBase(lambda x,y:x and y)

def psOr():
    binaryOpBase(lambda x,y:x or y)

def psNot():
    unaryOpBase(lambda x:not x)
