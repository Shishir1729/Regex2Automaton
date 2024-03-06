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
        # The number of states in the new FSA is the sum of the states in fsaX and fsaY
        numStates = fsaX.numStates + fsaY.numStates

        # The start states of the new FSA are the start states of fsaX
        startStates = fsaX.startStates

        # The final states of the new FSA are the final states of fsaY, shifted by the number of states in fsaX
        finalStates = [state+fsaX.numStates for state in fsaY.finalStates]

        # Initialize the transition table for the new FSA
        alphabetTransitions = {}

        # For each symbol in the alphabet
        for symbol in 'abc':
            alphabetTransitions[symbol] = []

            # Initialize the transition table for this symbol
            for state in range(numStates):
                alphabetTransitions[symbol].append([0]*numStates)

            # Copy the transitions from fsaX for this symbol
            for state in range(fsaX.numStates):
                alphabetTransitions[symbol][state] = fsaX.alphabetTransitions[symbol][state]
                alphabetTransitions[symbol][state].extend([0]*(fsaY.numStates))

            # For each state in fsaX, if it transitions to a final state on this symbol, add a transition to all start states in fsaY
            for state in range(fsaX.numStates):
                for i in range(fsaX.numStates):
                    if fsaX.alphabetTransitions[symbol][state][i] == 1 and i in fsaX.finalStates:
                        for j in range(fsaX.numStates, numStates):
                            if j - fsaX.numStates in fsaY.startStates:
                                alphabetTransitions[symbol][state][j] = 1

            # Copy the transitions from fsaY for this symbol, shifted by the number of states in fsaX
            for state in range(fsaX.numStates, numStates):
                alphabetTransitions[symbol][state] = [0] * fsaX.numStates + fsaY.alphabetTransitions[symbol][state-fsaX.numStates]

        # If any of the start states in fsaX are also final states, add the start states of fsaY as start states
        for state in fsaX.startStates:
            if state in fsaX.finalStates:
                startStates.extend([state + fsaX.numStates for state in fsaY.startStates])
                break

        # Add transitions on the empty string from each state to itself
        alphabetTransitions['e'] = [[1 if i == j else 0 for j in range(numStates)] for i in range(numStates)]

        # Create the new FSA
        fsa = NFA(numStates=numStates, startStates=startStates, finalStates=finalStates, alphabetTransitions=alphabetTransitions)

        return fsa
            

    # +
    def operatorPlus(self, fsaX, fsaY):
        # The number of states in the new FSA is the sum of the states in fsaX and fsaY
        fsaY.numStates = fsaX.numStates + fsaY.numStates

        # The start states of the new FSA are the start states of fsaY, shifted by the number of states in fsaX (We will add the start states of fsaX later)
        fsaY.startStates = [state+fsaX.numStates for state in fsaY.startStates]

        # The final states of the new FSA are the final states of fsaY, shifted by the number of states in fsaX (We will add the final states of fsaX later)
        fsaY.finalStates = [state+fsaX.numStates for state in fsaY.finalStates]

        # For each symbol in the alphabet
        for symbol in 'abc':
            # The transitions for this symbol in the new FSA are the transitions in fsaX followed by the transitions in fsaY
            fsaY.alphabetTransitions[symbol] = fsaX.alphabetTransitions[symbol] + fsaY.alphabetTransitions[symbol]

            # For each state in fsaY
            for state in range(fsaX.numStates, fsaY.numStates):
                # Add zeros at the beginning of the transition list for this state, to account for the new states from fsaX
                fsaY.alphabetTransitions[symbol][state] = [0]*fsaX.numStates + fsaY.alphabetTransitions[symbol][state]

            # For each state in fsaX
            for state in range(fsaX.numStates):
                # Copy the transitions from fsaX for this symbol
                fsaY.alphabetTransitions[symbol][state] = fsaX.alphabetTransitions[symbol][state]
                # Extend the transition list for this state with zeros, to account for the new states from fsaY
                fsaY.alphabetTransitions[symbol][state].extend([0]*(fsaY.numStates-fsaX.numStates))
        
        # Add transitions on the empty string from each state to itself
        fsaY.alphabetTransitions['e'] = [[1 if i == j else 0 for j in range(fsaY.numStates)] for i in range(fsaY.numStates)]

        # The start states of the new FSA are the start states of both fsaX and fsaY
        fsaY.startStates = fsaX.startStates + fsaY.startStates

        # The final states of the new FSA are the final states of both fsaX and fsaY
        fsaY.finalStates = fsaX.finalStates + fsaY.finalStates

        # Return the new FSA
        return fsaY
    
    
    # *
    def operatorStar(self, fsaX):
        # For each symbol in the alphabet
        for symbol in 'abc':
            # Add a new state to the FSA
            fsaX.alphabetTransitions[symbol].append([0]*(fsaX.numStates+1))

            for state in range(fsaX.numStates):
                # Extend the transition list for this state with a zero, to account for the new state
                fsaX.alphabetTransitions[symbol][state].append(0)

            # For each state in the FSA
            for state in range(fsaX.numStates):
                #If the state is a start state
                if state in fsaX.startStates:
                    # For each state in the FSA
                    for i in range(fsaX.numStates):
                        # If there is a transition from the current state to state i on this symbol
                        if fsaX.alphabetTransitions[symbol][state][i] == 1:
                            # Add a transition from the new state to state i on this symbol
                            fsaX.alphabetTransitions[symbol][fsaX.numStates][i] = 1
                # For each state in the FSA
                for i in range(fsaX.numStates):
                    # If there is a transition from the current state to state i on this symbol, and state i is a final state
                    if fsaX.alphabetTransitions[symbol][state][i] == 1 and i in fsaX.finalStates:
                        # Add a transition from the current state to the new state on this symbol
                        fsaX.alphabetTransitions[symbol][state][fsaX.numStates] = 1

            # For each start state in the FSA
            for state in fsaX.startStates:
                # For each state in the FSA
                for i in range(fsaX.numStates):
                    # If there is a transition from the current state to state i on this symbol where i is a final state.
                    if fsaX.alphabetTransitions[symbol][state][i] == 1 and i in fsaX.finalStates:
                        # Add a self-loop at the new state on this symbol
                        fsaX.alphabetTransitions[symbol][fsaX.numStates][fsaX.numStates] = 1

        # Add transitions on the empty string from each state to itself
        fsaX.alphabetTransitions['e'] = [[1 if i == j else 0 for j in range(fsaX.numStates+1)] for i in range(fsaX.numStates+1)]

        #The new state is the only start and final state
        fsaX.finalStates = [fsaX.numStates]
        fsaX.startStates = [fsaX.numStates]

        # Increase the number of states in the FSA
        fsaX.numStates += 1

        # Return the modified FSA
        return fsaX

    # a, b, c and e for epsilon
    def alphabet(self, symbol):
        # Create an FSA with a single state and no transitions
        if symbol == 'e':
            fsa = NFA(numStates=1, startStates=[0], finalStates=[0], alphabetTransitions={'a': [[0]], 'b': [[0]], 'c': [[0]], 'e': [[1]]})
            return fsa
        
        # Create an FSA with two states and transitions for the given symbol
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
        
