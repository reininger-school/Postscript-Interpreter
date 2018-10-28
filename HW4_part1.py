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
