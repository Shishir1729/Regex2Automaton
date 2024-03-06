import abc

# this class characterizes an automaton
class FSA:
    def __init__ (self, numStates = 0, startStates=None, finalStates=None, alphabetTransitions=None) :
        self.numStates = numStates
        self.startStates = startStates
        self.finalStates = finalStates
        self.alphabetTransitions = alphabetTransitions

class NFA(FSA):
    def simulate(self, ipStr):
        S = set(self.startStates)
        newS = set()
        for i in range(len(ipStr)):
            symbol = ipStr[i]
            tm = self.alphabetTransitions[symbol]
            for state in S:
                trs = tm[state]
                for tr in range(len(trs)):
                    if trs[tr] == 1:
                        newS.add(tr)
            S = set(newS)
            newS = set()
        if len(self.finalStates) > 0 and not S.isdisjoint(self.finalStates):
            print("String Accepted")
            return True
        else:
            print("String Rejected")
            return False

    def getNFA(self):
        return self

class ETree:
    root = None
    nfa = None
    class ETNode:
        def __init__(self, val=" ", left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    def compute(self, operands, operators):
            operator = operators.pop()
            if operator == "*":
                left = operands.pop()
                operands.append(self.ETNode(val=operator, left=left))
            elif operator == "+":
                right, left = operands.pop(), operands.pop()
                operands.append(self.ETNode(val=operator, left=left, right=right))
            elif operator == ".":
                right, left = operands.pop(), operands.pop()
                operands.append(self.ETNode(val=operator, left=left, right=right))

    def parseRegex(self, regex):
        operands, operators = [], []
        for i in range(len(regex)):
            if regex[i].isalpha():
                operands.append(self.ETNode(val=regex[i]))
            elif regex[i] == '(':
                operators.append(regex[i])
            elif regex[i] == ')':
                while operators[-1] != '(':
                    self.compute(operands, operators)
                operators.pop()
            else :
                operators.append(regex[i])
        while operators:
            self.compute(operands, operators)

        if len(operators) == 0:
            self.root = operands[-1]
        else :
            print("Parsing Regex failed.")

    def getTree(self):
        return self.root

    ###################################################################
    # IMPLEMENTATION STARTS AFTER THE COMMENT
    # Implement the following functions

    # In the below functions to be implemented delete the pass statement
    # and implement the functions. You may define more functions according
    # to your need.
    ###################################################################
    # .
    def operatorDot(self, fsaX, fsaY):
        numStates = fsaX.numStates + fsaY.numStates
        startStates = fsaX.startStates
        finalStates = [state+fsaX.numStates for state in fsaY.finalStates]
        alphabetTransitions = {}
        for symbol in 'abc':
            alphabetTransitions[symbol] = []
            for state in range(numStates):
                alphabetTransitions[symbol].append([0]*numStates)
            for state in range(fsaX.numStates):
                alphabetTransitions[symbol][state] = fsaX.alphabetTransitions[symbol][state]
                alphabetTransitions[symbol][state].extend([0]*(fsaY.numStates))
            for state in range(fsaX.numStates):
                for i in range(fsaX.numStates):
                    if fsaX.alphabetTransitions[symbol][state][i] == 1 and i in fsaX.finalStates:
                        for j in range(fsaX.numStates, numStates):
                            if j - fsaX.numStates in fsaY.startStates:
                                alphabetTransitions[symbol][state][j] = 1
            for state in range(fsaX.numStates, numStates):
                alphabetTransitions[symbol][state] = [0] * fsaX.numStates + fsaY.alphabetTransitions[symbol][state-fsaX.numStates]
        
        for state in fsaX.startStates:
            if state in fsaX.finalStates:
                startStates.extend([state + fsaX.numStates for state in fsaY.startStates])
                break

        alphabetTransitions['e'] = [[1 if i == j else 0 for j in range(numStates)] for i in range(numStates)]
        
        fsa = NFA(numStates=numStates, startStates=startStates, finalStates=finalStates, alphabetTransitions=alphabetTransitions)
        return fsa

        

    # +
    def operatorPlus(self, fsaX, fsaY):
        #add fsaX.numstates to all states of fsaY
        fsaY.numStates = fsaX.numStates + fsaY.numStates
        fsaY.startStates = [state+fsaX.numStates for state in fsaY.startStates]
        fsaY.finalStates = [state+fsaX.numStates for state in fsaY.finalStates]
        for symbol in 'abc':
            fsaY.alphabetTransitions[symbol] = fsaX.alphabetTransitions[symbol] + fsaY.alphabetTransitions[symbol]
            for state in range(fsaX.numStates, fsaY.numStates):
                #Add 0s in the beginning for the new states
                fsaY.alphabetTransitions[symbol][state] = [0]*fsaX.numStates + fsaY.alphabetTransitions[symbol][state]

            for state in range(fsaX.numStates):
                fsaY.alphabetTransitions[symbol][state] = fsaX.alphabetTransitions[symbol][state]
                fsaY.alphabetTransitions[symbol][state].extend([0]*(fsaY.numStates-fsaX.numStates))
        
        fsaY.alphabetTransitions['e'] = [[1 if i == j else 0 for j in range(fsaY.numStates)] for i in range(fsaY.numStates)]

        fsaY.startStates = fsaX.startStates + fsaY.startStates
        fsaY.finalStates = fsaX.finalStates + fsaY.finalStates
        return fsaY
    
    # *
    def operatorStar(self, fsaX):
        for symbol in 'abc':
            fsaX.alphabetTransitions[symbol].append([0]*(fsaX.numStates+1))
            for state in range(fsaX.numStates):
                fsaX.alphabetTransitions[symbol][state].append(0)
            
            for state in range(fsaX.numStates):
                if state in fsaX.startStates:
                    for i in range(fsaX.numStates):
                        if fsaX.alphabetTransitions[symbol][state][i] == 1:
                            fsaX.alphabetTransitions[symbol][fsaX.numStates][i] = 1
                for i in range(fsaX.numStates):
                    if fsaX.alphabetTransitions[symbol][state][i] == 1 and i in fsaX.finalStates:
                        fsaX.alphabetTransitions[symbol][state][fsaX.numStates] = 1

            
            #Decide self loop
            for state in range(fsaX.numStates):
                if state in fsaX.startStates:
                    for i in range(fsaX.numStates):
                        if fsaX.alphabetTransitions[symbol][state][i] == 1 and i in fsaX.finalStates:
                            fsaX.alphabetTransitions[symbol][fsaX.numStates][fsaX.numStates] = 1
            
        fsaX.alphabetTransitions['e'] = [[1 if i == j else 0 for j in range(fsaX.numStates+1)] for i in range(fsaX.numStates+1)]


            
        fsaX.numStates += 1
        fsaX.startStates = [fsaX.numStates-1]
        fsaX.finalStates = [fsaX.numStates-1]

        return fsaX

    # a, b, c and e for epsilon
    def alphabet(self, symbol):
        if symbol == 'e':
            fsa = NFA(numStates=1, startStates=[0], finalStates=[0], alphabetTransitions={'a': [[0]], 'b': [[0]], 'c': [[0]], 'e': [[1]]})
            return fsa
        elif symbol == 'a':
            fsa = NFA(numStates=2, startStates=[0], finalStates=[1], alphabetTransitions={'a': [[0,1], [0,0]], 'b': [[0,0], [0,0]], 'c': [[0,0], [0,0]], 'e': [[1,0], [0,1]]})
        elif symbol == 'b':
            fsa = NFA(numStates=2, startStates=[0], finalStates=[1], alphabetTransitions={'a': [[0,0], [0,0]], 'b': [[0,1], [0,0]], 'c': [[0,0], [0,0]], 'e': [[1,0], [0,1]]})
        elif symbol == 'c':
            fsa = NFA(numStates=2, startStates=[0], finalStates=[1], alphabetTransitions={'a': [[0,0], [0,0]], 'b': [[0,0], [0,0]], 'c': [[0,1], [0,0]], 'e': [[1,0], [0,1]]})    
        
        return fsa

    # Traverse the regular expression tree(ETree)
    # calling functions on each node and hence
    # building the automaton for the regular
    # expression at the root.
    def buildNFA(self, root):
        if root == None:
            print("Tree not available")
            exit(0)

        numStates = 0
        initialState = set()
        finalStates = set()
        transitions = {}

        # write code to populate the above datastructures for a regex tree
        if root.val == '.':
            fsaX = self.buildNFA(root.left)
            fsaY = self.buildNFA(root.right)
            fsa = self.operatorDot(fsaX, fsaY)
            return fsa

        elif root.val == '+':
            fsaX = self.buildNFA(root.left)
            fsaY = self.buildNFA(root.right)
            fsa = self.operatorPlus(fsaX, fsaY)
            return fsa
        elif root.val == '*':
            fsaX = self.buildNFA(root.left)
            fsa = self.operatorStar(fsaX)
            return fsa
        else:
            fsa = self.alphabet(root.val)
            return fsa

    ######################################################################