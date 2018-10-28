#programmer: Reid Reininger(charles.reininger@wsu.edu)
#date: 10/24/18
#desc: (intended for Unix/Linux)

#globals
opstack = []
dictstack = [{}]

#operand stack operators
def opPop():
    """Pop opstack."""
    return opstack.pop()

def opPush(value):
    """Push value onto opstack."""
    return opstack.append(value)

def opPopn(n):
    """Pop n values from opstack and return as tuple"""
    if len(opstack) >= n:
        return tuple(opPop() for x in range(n))
    else:
        print('error: not enough items in opstack')

#dictionary stack operators
def dictPop():
    """Pop dictstack."""
    return dictstack.pop()

def dictPush():
    """Push empty dict onto dictstack."""
    return dictstack.append({})

def define(name, value):
    """Add name:value pair to top dict in dictstack."""
    dictstack[-1][name] = value

def lookup(name):
    """Return most recently defined value for name."""
    for x in reversed(dictstack):
        for key in x:
            if key == name:
                return x[key]
    else:
        print('error: name not found')

#Arithmetic and comparison operators
def add():
    """Pop opstack twice and push sum onto opstack."""
    op1, op2 = opPopn(2)
    opPush(op1 + op2)

def sub():
    """Pop opstack twice and push op1 - op2 onto opstack."""
    op1, op2 = opPopn(2)
    opPush(op1 - op2)

def mul():
    """Pop opstack twice and push product onto opstack."""
    op1, op2 = opPopn(2)
    opPush(op1 * op2)

def div():
    """Pop opstack twice and push op1 / op2 onto opstack."""
    op1, op2 = opPopn(2)
    opPush(op1 / op2)

def mod():
    """Pop opstack twice and push op1 % op2 ont opstack."""
    op1, op2 = opPopn(2)
    opPush(op1 % op2)
