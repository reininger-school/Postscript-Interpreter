#programmer: Reid Reininger(charles.reininger@wsu.edu)
#date: 10/24/18
#desc: (intended for Unix/Linux)

opstack = []

def opPop():
    return opstack.pop()

def opPush(value):
    return opstack.append(value)
