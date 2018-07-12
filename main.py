'''
CSE305: HW2 SPRING 2016
A very basic interpreter for a pseudo-language with one 
word commands on each line. It takes in an input file, executes
the commands on each line, the pushes the result to an output file

Created on Feb 27, 2016

@author: Ron
'''
currEnv = 0

""" 
    Prints the contents of the default stack
    to a given file but removes all token codes.
"""
def outputStack():
    result = ''
    while len(stackList[0]) > 0:
        toOut = str(stackList[0].pop())
        result += (toOut[0:toOut.index("[")] + "\n")
    return result
        
""" 
    Pushes a string that has both a value
    and its token code to the stack
"""
def pushToStackWTag(x):
    stackList[currEnv].append(x)

""" 
    Concatenates a string and a token 
    that is to be pushed to the stack.
"""  
def pushToStack(x, token):
    stackList[currEnv].append(x + token)

""" 
    Pops an item from the current stack.
    If there are no items, an error is pushed
    to the stack
"""
def popStack():
    if len(stackList[currEnv]) > 0:
        stackList[currEnv].pop();
    else: 
        pushToStack(":error:", "[error]")

"""
    Overall, this function performs mathematical operations
    including *, -, /, +, %, ==, and less than on the top two elements
    on the current stack. It will take either integer literals or names
    with in-scope bond values which can be converted to integers. If there 
    are not two integer elements available to operate on, the stack will revert 
    back to its prior stack with an error message pushed to the top.
"""
def arithmetic(opType):
    if len(stackList[currEnv]) >= 2:
        s1 = stackList[currEnv].pop();
        s2 = stackList[currEnv].pop();
        temp1 = ""
        temp2 = ""

        for i in range(0, currEnv+1):  
            if s1.find("[name]") != -1 and s1 in mapList[i]:
                temp1 = mapList[i].get(s1)
                temp1 = str(temp1)[0:temp1.index("[")]
        
            if s2.find("[name]") != -1 and s2 in mapList[i]:
                temp2 = mapList[i].get(s2)
                temp2 = str(temp2)[0:temp2.index("[")]
        
        if s1.find("[int]") != -1:
            temp1 = str(s1)[0:s1.index("[")] 
            
        if s2.find("[int]") != -1:
            temp2 = str(s2)[0:s2.index("[")] 
        
        try:            
            operand1 = int(temp1)
            operand2 = int(temp2)
            
            if opType.find("add") != -1:
                pushToStack(str(operand2 + operand1), "[int]")
            elif  opType.find("sub") != -1:
                pushToStack(str(operand2 - operand1), "[int]")
            elif  opType.find("mul") != -1:
                pushToStack(str(operand2 * operand1), "[int]")
            elif  opType.find("div") != -1:
                pushToStack(str(operand2 / operand1), "[int]")
            elif  opType.find("rem") != -1:
                pushToStack(str(operand2 % operand1), "[int]")
            elif  opType.find("equal") != -1:
                if operand1 == operand2:
                    pushToStack(":true:", "[bool]");
                else: 
                    pushToStack(":false:", "[bool]");
            elif opType.find("lessThan") != -1:
                if operand1 > operand2:
                    pushToStack(":true:", "[bool]");
                else: 
                    pushToStack(":false:", "[bool]");          
        except ValueError:
            pushToStackWTag(s2)
            pushToStackWTag(s1)
            pushToStack(":error:", "[error]")
    else:
        pushToStack(":error:", "[error]")

"""negation takes the top element in the stack
and negates it, if it is a number. If not a number,
it will push an error message to the stack """        
def negation(number):
    if len(stackList[currEnv]) >= 1: 
        negatee = stackList[currEnv].pop()
        
        
        for i in range(0, currEnv+1):     
            if negatee.find("[name]") != -1 and negatee in mapList[i]:
                negatee = mapList[i].get(negatee)
                negatee = str(negatee)[0:negatee.index("[")]
        
        try:
            negatee = int(negatee)
            stackList[currEnv].append((-1) * negatee)
        except ValueError:
            stackList[currEnv].append(negatee)
            pushToStack(":error:", "[error]")

""" swap  switches the top two elements in  a stack
unless there are less than two elements. If less than to
an error string is pushed onto the stack """
def swap():
    if len(stackList[currEnv]) >= 2:
        s1 = stackList[currEnv].pop()
        s2 = stackList[currEnv].pop()
        stackList[currEnv].append(s1)
        stackList[currEnv].append(s2)
    else:
        pushToStack(":error:", "[error]")
"""
   Takes top two elements on the stack and performs a 
   logical ANDing operation on them(if possible). If both elements  
   are bool values, it will consume those elements and push the result
   onto the stack. Otherwise, the elements will remain and an error message
   will be pushed.
"""
def anding():
    if len(stackList[currEnv]) >= 2:
        s1 = stackList[currEnv].pop()
        s2 = stackList[currEnv].pop()
        
        for i in range(0, currEnv+1):    
            if s1.find("[name]") != -1 and s1 in mapList[i]:
                s1 = mapList[i].get(s1)
                s1 = str(s1)[0:s1.index("[")]
        
            if s2.find("[name]") != -1 and s2 in mapList[i]:
                s2 = mapList[i].get(s2)
                s2 = str(s2)[0:s2.index("[")]
        
        if s1.find('[bool]') != -1 and s2.find('[bool]') != -1:
            if s1.find(':true:') != -1 and s2.find(':true:') != -1:
                pushToStack(":true:", "[bool]")
            else:
                pushToStack(":false:", "[bool]")
        else:
            pushToStackWTag(s2)
            pushToStackWTag(s1)
            pushToStack(":error:", "[error]")     
    else:
        pushToStack(":error:", "[error]")

"""
   oring has the same functionality as anding()
   except that it applies a logical ORing operation instead.
"""
def oring():
    if len(stackList[currEnv]) >= 2:
        s1 = stackList[currEnv].pop()
        s2 = stackList[currEnv].pop()
        
        for i in range(0, currEnv+1):  
            if s1.find("[name]") != -1 and s1 in mapList[i]:
                s1 = mapList[i].get(s1)
                s1 = str(s1)[0:s1.index("[")]
        
            if s2.find("[name]") != -1 and s2 in mapList[i]:
                s2 = mapList[i].get(s2)
                s2 = str(s2)[0:s2.index("[")]
        
        if s1.find('[bool]') != -1 and s2.find('[bool]') != -1:
            if s1.find(':true:') != -1 or s2.find(':true:') != -1:
                pushToStack(":true:", "[bool]")
            else:
                pushToStack(":false:", "[bool]")
        else:
            pushToStackWTag(s2)
            pushToStackWTag(s1)
            pushToStack(":error:", "[error]")       
    else:
        pushToStack(":error:", "[error]")
 
"""
   noting is similar to oring() and anding() 
   except it only acts on one element. Performs a
   logical NOT on the element, consumes it, and pushes the result to the stack.
"""       
def noting():
    if len(stackList[currEnv]) > 0:
        s1 = stackList[currEnv].pop()
        
        for i in range(0, currEnv+1):    
            if s1.find("[name]") != -1 and s1 in mapList[i]:
                s1 = mapList[i].get(s1)
                s1 = str(s1)[0:s1.index("[")]
        
        
        if s1.find('[bool]') != -1:
            if s1.find(':true:') != -1:
                pushToStack(":false:", "[bool]")
            elif s1.find(':false:') != -1:
                pushToStack(":true:", "[bool]")
        else: 
            pushToStackWTag(s1);
            pushToStack(":error:", "[error]")    
    else:
        pushToStack(":error:", "[error]")
        
""" 
    Searches through in-scope bindings
    and returns the key of a given variable name.
    The functions returns the empty string otherwise
"""
def getValue(name):
    if name.find('[name]') != -1:
        for i in range(0, currEnv+1): 
            if name in mapList[i]:
                return mapList[i].get(name)
    else:
        return ""
    return ""

""" 
    isBindable determines if a string is a valid value that can be
    bound to a name. It must be of type bool, int, unit, quote, or be
    a name which is already bound to a value(must be in-scope)
"""            
def isBindable(val):
    if val.find('[bool]') != -1 or val.find('[int]') != -1 or val.find('[unit]') != -1 or val.find('[quote]') != -1:
        return True
    elif not(getValue(val) == ""):
        return True
    else:
        return False

""" 
    binding binds a name to a valid value. If two elements are on the stack,
    it pops the two elements off where the value is the first one popped and
    the name is the second one popped. It will either apply the literal value given
    or the value of a bound, in-scope name given as a value to the name. If successful,
    the binding will be stored in a local map and a unit will be pushed to the stack. Otherwise,
    it will revert to its normal state and push an error onto the stack.
"""   
def binding():
    if len(stackList[currEnv]) > 1: 
        print("binding")          
        valToBind = stackList[currEnv].pop()  
        name = stackList[currEnv].pop()
        if isBindable(valToBind) and name.find('[name]') != -1:
            if valToBind.find('[name]') != -1:
                print(valToBind)
                (mapList[currEnv])[name] = getValue(valToBind)
                pushToStack(":unit:", "[unit]")
            else:
                mapList[currEnv][name] = valToBind
                pushToStack(":unit:", "[unit]")
        else:
            pushToStackWTag(name)
            pushToStackWTag(valToBind)
            pushToStack(":error:", "[error]")
    else:
        pushToStack(":error:", "[error]")
        

""" 
    Pops the top three elements from the stack(x,y,z). If the last element z
    is of type boolean,it will check if it is true or false. if true, x will be
    pushed back to the stack. If false, y will be pushed. If unsuccessful, it reverts
    back to the previous state and an error is pushed onto the stack.
"""     
def iff():
    if len(stackList[currEnv]) >= 3:
        x = stackList[currEnv].pop() 
        y = stackList[currEnv].pop() 
        z = stackList[currEnv].pop() 
        
        for i in range(0, currEnv+1):    
            if z.find("[name]") != -1 and z in mapList[i]:
                z = mapList[i].get(z)
                z = str(z)[0:z.index("[")]
        
        
        if z.find('[bool]') != -1:
            if z.find(':true:') != -1:
                pushToStackWTag(x)
            elif z.find(':false:') != -1:
                pushToStackWTag(y)
        else: 
            pushToStackWTag(z)
            pushToStackWTag(y)
            pushToStackWTag(x)
            pushToStack(":error:", "[error]")
    else:
        pushToStack(":error:", "[error]")  

""" 
    It moves the program into a new environment when a "let" statement is given
    It does this buy incrementing the variance properties for the environments.
    Each environment has its own currEnv index, stack, and binding map. 
    currEnv is incremented to keep track of which environment it is currently in 
    and to access its stack and/or binding map throughout the course of its lifetime.  
"""          
def createEnvironment():
    global currEnv
    currEnv += 1 
    stackList.append([])
    mapList.append(dict())

""" 
    In conjunction with createEnvironment, this function moves us out of the
    current environment to most previous one when "end" is given. It also 
    pushes the last stack element of the current stack onto the previous environments   
    stack. 
"""  
def endEnvironment():
    global currEnv
    if len(stackList[currEnv]) >= 1:
        stackList[currEnv - 1].append(stackList[currEnv].pop())
        
    stackList.pop(currEnv)
    mapList.pop(currEnv)
    currEnv = currEnv - 1
        
""" operation maps every accepted token 
    for the language and maps it to an operation """
def operation(word):
    x = word.replace("push", "").strip()
    if word.find("push") != -1:
        try:
            if float(x).is_integer():
                pushToStack(x, "[int]")
            else:
                pushToStack(":error:", "[error]") 
                
        except ValueError:
            if x.find("\"") != -1:
                pushToStack(x.strip("\""), "[quote]")
            else:
                pushToStack(x, "[name]")

    elif  word.find('pop') != -1: 
        popStack() 
    elif word.find(':true:') != -1: 
        pushToStack(word, "[bool]") 
    elif word.find(':false:') != -1: 
        pushToStack(word, "[bool]")
    elif word.find(':error:') != -1:
        pushToStack(word, "[error]") 
    elif word.find("add") != -1:
        print(word)
        arithmetic(word)
    elif word.find('sub') != -1: 
        arithmetic(word) 
    elif word.find('mul') != -1: 
        arithmetic(word)
    elif word.find('div') != -1:
        arithmetic(word) 
    elif word.find('rem') != -1: 
        arithmetic(word)
    elif word.find('neg') != -1:
        negation(word)
    elif word.find('swap') != -1: 
        swap()        
    elif word.find('and') != -1:
        anding()
    elif word.find('or') != -1:
        oring()
    elif word.find('not') != -1:
        noting()
    elif word.find('equal') != -1: 
        arithmetic(word)
    elif word.find('lessThan') != -1: 
        arithmetic(word)
    elif word.find('bind') != -1: 
        binding();
    elif word.find('if') != -1: 
        iff();
    elif word.find('let') != -1:    
        createEnvironment()
    elif word.find('end') != -1:    
        endEnvironment()
        
def main(input):
    inputFile = open(input, "r")
    """Collection of all local stacks"""
    global stackList
    stackList = []
    stackList.append([])
    
    """Collection of all local bindings"""
    global mapList
    mapList = []
    mapList.append(dict())  
    
    """current environment index"""
    global currEnv
    currEnv = 0
    
    """iterate over input file"""   
    for text in inputFile:        
        tokenize = text.splitlines()
        for line in tokenize:    
            operation(line)       
    inputFile.close()
    return outputStack()


