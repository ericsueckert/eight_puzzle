'''
Eric Eckert
'''

#<METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Rubik's Cube"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['E. Eckert', 'Derek Wang']
PROBLEM_CREATION_DATE = "19-APR-2017"
PROBLEM_DESC=\
        '''
Eight Puzzle uses generic Python 3
'''

#</METADATA>

#<COMMON_CODE>

def can_move(s,From,To):
    try:
        #print("state")

        if not s.d[From]==0: return False
        else: return True

    except (Exception) as e:
        print(e)

def move(s,From,To):
    news = s.__copy__()
    d2 = news.d
    sf=d2[From]
    d2[From] = d2[To]
    d2[To] = sf
    return news

def goal_test(s):
    return s.d == complete

def goal_message(s):
    return "The Eight Puzzle is complete!"

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)

def h_hamming(state):
    "Counts the number of disks NOT at the destination peg."
    n = 0
    for i in range(0,9):
        if not state.d[i] == complete[i]:
            n += 1

    return n

def h_euclidean(s):
    total = 0.0
    for i in range(0,9):
        horizontal = 0.0
        vertical = 0.0
        n = s.d[i]
        if not i%3==n%3:
            if i%3==1 or n%3==1:
                horizontal += 1
            else:
                horizontal += 2
        if not i//3==n//3:
            if i//3==1 or n//3==1:
                vertical += 1
            else:
                vertical += 2

        #print("tile: " + str(i))
        #print(horizontal)
        #print(vertical)
        hypotenuse = (horizontal**2+vertical**2)**(0.5)
        total += hypotenuse
        #print(hypotenuse)
    return total

def h_manhattan(s):
    total = 0
    for i in range(0,9):
        horizontal = 0
        vertical = 0
        n = s.d[i]
        if not i%3==n%3:
            if i%3==1 or n%3==1:
                horizontal = 1
            else:
                horizontal = 2
        if not i//3==n//3:
            if i//3==1 or n//3==1:
                vertical = 1
            else:
                vertical = 2
        #print("tile: " + str(i))
        #print(horizontal)
        #print(vertical)

        total = total + horizontal + vertical
    return total

def h_custom(s):
    'My custom heuristic takes the average of hamming, euclidean, and manhattan heuristics.'
    total = h_hamming(s) + h_euclidean(s) + h_manhattan(s)
    return total/3

#</COMMON_CODE>

#<COMMON_DATA>
complete = [0,1,2,3,4,5,6,7,8]
#</COMMON_DATA>


#<STATE>
class State():
    def __init__(self, d):
        self.d = d

    def __str__(self):
        # Produces a brief textual description of a state.
        d = self.d
        txt = ""
        for i in range(0, 9):
            txt = txt+"["+str(d[i])+"]"
            if i%3==2:
                txt+="\n"

        return txt

    def __eq__(self, s2):
        if not (type(self)==type(s2)): return False
        d1 = self.d; d2 = s2.d
        return d1==d2

    def __hash__(self):
        return (str(self)).__hash__()

    def __copy__(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State([])
        for i in range(0, 9):
            news.d.append(self.d[i])
        return news

    def __lt__(self, s2):
        return True

#</STATE>


#<INITIAL_STATE>
a = [1, 0, 2, 3, 4, 5, 6, 7, 8]
b = [3, 1, 2, 4, 0, 5, 6, 7, 8]
c = [1, 4, 2, 3, 7, 0, 6, 8, 5]
a10 = [4, 5, 0, 1, 2, 3, 6, 7, 8]
a12 = [3, 1, 2, 6, 8, 7, 5, 4, 0]
a14 = [4, 5, 0, 1, 2, 8, 3, 7, 6]
a16 = [0, 8, 2, 1, 7, 4, 3, 6, 5]
INITIAL_STATE = State(a10)
CREATE_INITIAL_STATE = lambda: INITIAL_STATE

#</INITIAL_STATE>

#<OPERATORS>
# Calculate all possible legal movement combinations
combinations = []
for i in range(0, 9):
    for j in range(0, 9):
        if not i==j:
            combinations.append((i,j))

remove = []
for pair in combinations:
    a = pair[0]
    b = pair[1]
    if (a%3==0 and b%3==2) or (a%3==2 and b%3==0) or (a<3 and b>5) or (a>5 and b<3):
        remove.append(pair)
        continue

    if a==b+1 or a==b-1 or a==b+3 or a==b-3: continue
    remove.append(pair)

for pair in remove:
    combinations.remove(pair)

#print(combinations)


#peg_combinations = [('tile '+str(a),'tile '+str(b)) for (a,b) in combinations]
OPERATORS = [Operator("Move tile from position "+str(p)+" to position "+str(q),
                      lambda s,p1=p,q1=q: can_move(s,p1,q1),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s,p1=p,q1=q: move(s,p1,q1) )
             for (p,q) in combinations]
#</OPERATORS>

#<GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>


#<HEURISTICS> (optional)
HEURISTICS = {'h_hamming': h_hamming, 'h_euclidean':h_euclidean, 'h_manhattan': h_manhattan, 'h_custom': h_custom}
#</HEURISTICS>
