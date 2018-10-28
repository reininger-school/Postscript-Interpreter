#programmer: Reid Reininger(charles.reininger@wsu.edu)
#date: 10/24/18
#desc: (intended for Unix/Linux)

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
    """Pop opstack and return None on failure."""
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
    """Return most recently defined value for name."""
    for x in reversed(dictstack):
        for key in x:
            if key == name:
                return x[key]
    else:
        print('error: name not found')

#helper functions
def isNumeric(*args):
    """Return true if all args are numeric."""
    for x in args:
        if not isinstance(x, Number):
            return False
    else:
        return True

def opSize():
    """Return number of values in opstack."""
    return len(opstack)

def dictSize():
    """Return number of dicitonaries in dictstack."""
    return len(dictstack)

#Arithmetic and comparison operators
def add():
    """Pop opstack twice and push sum onto opstack."""
    op2, op1 = opPopn(2)
    opPush(op1 + op2)

def sub():
    """Pop opstack twice and push op1 - op2 onto opstack."""
    op2, op1 = opPopn(2)
    opPush(op1 - op2)

def mul():
    """Pop opstack twice and push product onto opstack."""
    op2, op1 = opPopn(2)
    opPush(op1 * op2)

def div():
    """Pop opstack twice and push op1 / op2 onto opstack."""
    op2, op1 = opPopn(2)
    opPush(op1 / op2)

def mod():
    """Pop opstack twice and push op1 % op2 ont opstack."""
    op2, op1 = opPopn(2)
    opPush(op1 % op2)

def neg():
    """Pop opstack and push negation onto opstack."""
    op1 = opPop()
    opPush(-op1)

def lt():
    """Pop opstack twice and push result of op1<op2 onto opstack."""
    op2, op1 = opPopn(2)
    opPush(op1 < op2)

def gt():
    """Pop opstack twice and push result of op1>op2 onto opstack."""
    op2, op1 = opPopn(2)
    opPush(op1 > op2)

def eq():
    """Pop opstack twice and push result of op1==op2 onto opstack."""
    op2, op1 = opPopn(2)
    opPush(op1 == op2)
