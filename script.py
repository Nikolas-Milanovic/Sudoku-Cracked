import numpy as np
from typing import Tuple
import random
import time
import copy


#BACKTRACING ONLY

# Variables:
startTime = time.time()
problem = "easy.csv"
N = 9
B = 3
nodesExpanded = 0
CSVData = open(problem)
assignment = np.loadtxt(CSVData, delimiter=",")


cols = [set() for i in range(N)]
rows = [set() for i in range(N)]
boxes = [set() for i in range(N)]

zeros = list()
lenZeros = 0 
zeroIndex = 0


# init data
for i in range(N):
    for j in range(N):
        value = assignment[i][j]
        if value == 0:
            zeros.append((i, j))
        else:
            rows[i].add(value)
            cols[j].add(value)
            boxIndex = (int(i/B)*B) + int(j/B)
            boxes[boxIndex].add(value)

random.shuffle(zeros)
lenZeros = len(zeros)

print("original assignment:")
print(assignment)


# Helper Functions:
def selectUnassignedVariable() -> Tuple[int, int]:
    global zeroIndex
    ret = zeros[zeroIndex]
    zeroIndex+=1
    return ret


def orderDomainValues(i: int, j: int) -> list():
    boxIndex = (int(i/B)*B) + int(j/B)
    values = list()
    for value in range(1, N+1, 1):
        if (value in rows[i] or value in cols[j] or value in boxes[boxIndex]):
            continue
        values.append(value)

    random.shuffle(values)
    return values


# checks if assignment[i][j]=value is consistent
def isConsistent(i: int, j: int, value: int) -> bool:
    boxIndex = (int(i/B)*B) + int(j/B)
    if (value in rows[i] or value in cols[j] or value in boxes[boxIndex]):
        return False
    return True


def assign(i: int, j: int, value: int) -> None:
    boxIndex = (int(i/B)*B) + int(j/B)
    original = assignment[i][j]
    assignment[i][j] = value

    if (value == 0):
        rows[i].remove(original)
        cols[j].remove(original)
        boxes[boxIndex].remove(original)

    else:
        rows[i].add(value)
        cols[j].add(value)
        boxes[boxIndex].add(value)


def backtrackingSearch() -> bool:
    return recursiveBacktracking()


def recursiveBacktracking() -> bool:
    global nodesExpanded, zeroIndex
    nodesExpanded+=1
    if zeroIndex==lenZeros:
        return True
    i, j = selectUnassignedVariable()
    for value in orderDomainValues(i, j):
        assign(i, j, value)
        if recursiveBacktracking():
            return True
        else:
            assign(i, j, 0)
    zeroIndex-=1
    return False


# if backtrackingSearch():
#     print("SOLUTION FOUND!")
# else:
#     print("SOLUTION DNE!")
# print(assignment)
# print("Number of Nodes Expanded: ", nodesExpanded)
# print("Run Time (B): ", time.time()-startTime)
# #print(nodesExpanded,",",time.time()-startTime)






















































# FORWARD CHECKING IMPL
problem = "evil.csv"
startTime = time.time()
N = 9
B = 3
CSVData = open(problem)
assignment = np.loadtxt(CSVData, delimiter=",")
nodesExpanded = 0


zeros = list()
lenZeros = 0 
zeroIndex = 0
domains = [[set(list(range(1,N+1,1))) for j in range(N)] for i in range(N)]




def removeFromDomains(i: int, j: int, value: int) -> None:
    boxi, boxj = int(i/B)*B, int(j/B)*B
    for k in range(N):
        if domains[k][j]!=None and value in domains[k][j]: domains[k][j].remove(value)
        if domains[i][k]!=None and value in domains[i][k]: domains[i][k].remove(value)
        if domains[boxi+int(k/B)][boxj+(k % B)]!=None and value in domains[boxi+int(k/B)][boxj+(k % B)]: 
            domains[boxi+int(k/B)][boxj+(k % B)].remove(value)
            #print("i,j: ",boxi+int(k/B),boxj+(k % B))
            #print(value)


# print(domains)
# init data
for i in range(N):
    for j in range(N):
        value = assignment[i][j]
        if value == 0:
            zeros.append((i, j))
        else:
            domains[i][j]=None
            removeFromDomains(i,j,value)
          
random.shuffle(zeros)
lenZeros = len(zeros)
#zeros = [(8, 0), (4, 6), (1, 4), (1, 8), (4, 1), (2, 4), (5, 8), (4, 4), (2, 8), (5, 3), (8, 8), (0, 3), (7, 0), (3, 0), (6, 8), (6, 0), (3, 6), (0, 0), (7, 8), (4, 5), (1, 7), (5, 0), (4, 2), (7, 1), (6, 4), (4, 7), (1, 0), (5, 1), (4, 0), (1, 5), (3, 8), (3, 5), (1, 1), (0, 7), (7, 3), (8, 1), (2, 0), (7, 7), (8, 5), (0, 8), (4, 8), (3, 7), (4, 3), (7, 4), (5, 2)]
#print(zeros)

# print("original assignment:")
# print(assignment)
#print(domains)

domainsLevels = [None] * lenZeros
# domainsLevels[0] = domains

# Helper Functions:
def selectUnassignedVariable_F() -> Tuple[int, int]:
    global zeroIndex, domains
    
    ret = zeros[zeroIndex]
    domainsLevels[zeroIndex] = copy.deepcopy(domains)

    zeroIndex+=1
    return ret

def isConsistent_F(i: int, j: int, value: int) -> bool:
    global domains
    boxi, boxj = int(i/B)*B, int(j/B)*B
    #Note, assignment[i][j]==value is consistent, since domains[i][j] contains only feasible variables
    #Arc Consitency Check:

    removeFromDomains(i,j,value)
    # print(domains)

    flag = True
    for k in range(N):
        if (domains[k][j] !=None and k!= i and len(domains[k][j]) == 0 and assignment[k][j]==0):
            #print(domains[k][j])
            #print("k,j",k,j)
            flag = False
            break
        if (domains[i][k] !=None and  k!= j  and len(domains[i][k]) == 0 and assignment[i][k]==0):
            flag = False
            #print(domains[i][k])
            #print("i,k",i,k)
            break
        if (domains[boxi+int(k/B)][boxj+(k % B)]!=None 
            and boxi+int(k/B)!=i and boxj+(k % B)!=j 
            and len(domains[boxi+int(k/B)][boxj+(k % B)]) == 0 and assignment[boxi+int(k/B)][boxj+(k % B)]==0):
            flag = False
            #print(domains[boxi+int(k/B)][boxj+(k % B)])
            #print("box",boxi+int(k/B),boxj+(k % B))
            break
    
    if(flag==False):
        domains = copy.deepcopy(domainsLevels[zeroIndex-1])
    return flag


def orderDomainValues_F(i: int, j: int) -> list():
    values = list(domains[i][j])
    random.shuffle(values)
    return values


def backtrackingSearch_F() -> bool:
    return recursiveBacktracking_F()


def recursiveBacktracking_F() -> bool:
    global nodesExpanded, zeroIndex, domains
    nodesExpanded+=1
    if zeroIndex==lenZeros:
        return True
    i, j = selectUnassignedVariable_F()
    #print(assignment)
    for value in orderDomainValues_F(i, j):
        if isConsistent_F(i, j, value):
            #removeFromDomains(i, j, value)
            assignment[i][j]=value
            #print(assignment)
            if recursiveBacktracking_F():
                return True
            else:
                #assign_F(i, j, 0)
                assignment[i][j]=0
                domains = copy.deepcopy(domainsLevels[zeroIndex-1])
    zeroIndex-=1
    return False


# if backtrackingSearch_F():
#     print("SOLUTION FOUND!")
# else:
#     print("SOLUTION NOT FOUND!")
# print(assignment)
# print("Number of Nodes Expanded: ", nodesExpanded)

# print("Run Time (B+F): ", time.time()-startTime)


































# FORWARD CHECKING + HEURISTICS IMPL

problem = "medium.csv"
startTime = time.time()
N = 9
B = 3
CSVData = open(problem)
assignment = np.loadtxt(CSVData, delimiter=",")
nodesExpanded = 0


zeros = list()
lenZeros = 0 
zeroIndex = 0
domains = [[set(list(range(1,N+1,1))) for j in range(N)] for i in range(N)]

# constraining = [[20]*N for i in range(20)]

# def removeFromConstraining(i: int, j: int, value: int) -> None:
#     boxi, boxj = int(i/B)*B, int(j/B)*B
#     for k in range(N):
#         if assignment[k][j]==0: constraining[k][j]-=1
#         if assignment[i][k]==0: constraining[i][k]-=1
#         if assignment[boxi+int(k/B)][boxj+(k % B)]==0: constraining[boxi+int(k/B)][boxj+(k % B)]-=1


def removeFromDomains(i: int, j: int, value: int) -> None:
    boxi, boxj = int(i/B)*B, int(j/B)*B
    for k in range(N):
        if domains[k][j]!=None and value in domains[k][j]: domains[k][j].remove(value)
        if domains[i][k]!=None and value in domains[i][k]: domains[i][k].remove(value)
        if domains[boxi+int(k/B)][boxj+(k % B)]!=None and value in domains[boxi+int(k/B)][boxj+(k % B)]: 
            domains[boxi+int(k/B)][boxj+(k % B)].remove(value)
            #print("i,j: ",boxi+int(k/B),boxj+(k % B))
            #print(value)


# print(domains)
# init data
for i in range(N):
    for j in range(N):
        value = assignment[i][j]
        if value == 0:
            zeros.append((i, j))
        else:
            domains[i][j]=None
            # removeFromConstraining(i,j,value)
            removeFromDomains(i,j,value)
          
# random.shuffle(zeros)
lenZeros = len(zeros)
#print(zeros)

# print("original assignment:")
# print(assignment)
#print(domains)

domainsLevels = [None] * lenZeros
# constrainingLevels = [None] * lenZeros
# domainsLevels[0] = domains

# Helper Functions:

def getNumLeastConstraing(i: int, j:int, value: int) -> int:
    boxi, boxj = int(i/B)*B, int(j/B)*B
    num = 0
    for k in range(N):
        if k!= j and value in domains[k][j]: num+=1
        if k!= i and value in domains[i][k]: num+=1
        if boxi+int(k/B)!=i and [boxj+(k % B)]!=j and value in domains[boxi+int(k/B)][boxj+(k % B)]: num+=1 
    return num

def getNumConstraing_F_B(i: int, j: int) -> int:
    boxi, boxj = int(i/B)*B, int(j/B)*B
    num = 0
    for k in range(N):
        if k!= j and assignment[k][j]==0: num+=1
        if k!= i and assignment[i][k]==0: num+=1
        if boxi+int(k/B)!=i and [boxj+(k % B)]!=j and assignment[boxi+int(k/B)][boxj+(k % B)]==0: num+=1 
    return num

def selectUnassignedVariable_F_B() -> Tuple[int, int]:
    global zeroIndex, domains
    domainsLevels[zeroIndex] = copy.deepcopy(domains)
    # constrainingLevels[zeroIndex] = copy.deepcopy(constraining)
    zeroIndex+=1 #this is now used to check for valid solution 


    #MRV
    minMRV = [zeros[0]]
    minI,minJ = zeros[0]
    for k in range(1,lenZeros,1):
        i,j = zeros[k]
        if(assignment[i][j]==0 and len(domains[i][j]) < len(domains[minI][minJ])):
            minMRV = [zeros[k]]
            minI,minJ = zeros[zeroIndex]
        elif(assignment[i][j]==0 and len(domains[i][j]) == len(domains[minI][minJ])):
            minMRV.append(zeros[zeroIndex])
            

    
    if(len(minMRV)>=2):
        #tie break with most constraining variable
        maxConstraining = [minMRV[0]]
        i,j = minMRV[0]
        maxVal = getNumConstraing_F_B(i,j)
        for k in range(1,len(minMRV),1):
            i, j = minMRV[k]
            val = getNumConstraing_F_B(i,j)
            if  val < maxVal:
                maxVal = val
                maxConstraining = [minMRV[k]]
            if  val == maxVal:
                maxConstraining.append(minMRV[k])
        if len(maxConstraining) >= 2:
            return random.choice(maxConstraining)
        return minMRV[0]
    
    return minMRV[0]
    
    

def isConsistent_F_B(i: int, j: int, value: int) -> bool:
    global domains
    boxi, boxj = int(i/B)*B, int(j/B)*B
    #Note, assignment[i][j]==value is consistent, since domains[i][j] contains only feasible variables
    #Arc Consitency Check:

    removeFromDomains(i,j,value)
    # print(domains)

    flag = True
    for k in range(N):
        if (domains[k][j] !=None and k!= i and len(domains[k][j]) == 0 and assignment[k][j]==0):
            #print(domains[k][j])
            #print("k,j",k,j)
            flag = False
            break
        if (domains[i][k] !=None and  k!= j  and len(domains[i][k]) == 0 and assignment[i][k]==0):
            flag = False
            #print(domains[i][k])
            #print("i,k",i,k)
            break
        if (domains[boxi+int(k/B)][boxj+(k % B)]!=None 
            and boxi+int(k/B)!=i and boxj+(k % B)!=j 
            and len(domains[boxi+int(k/B)][boxj+(k % B)]) == 0 and assignment[boxi+int(k/B)][boxj+(k % B)]==0):
            flag = False
            #print(domains[boxi+int(k/B)][boxj+(k % B)])
            #print("box",boxi+int(k/B),boxj+(k % B))
            break
    
    if(flag==False):
        domains = copy.deepcopy(domainsLevels[zeroIndex-1])
    return flag


def orderDomainValues_F_B(i: int, j: int) -> list():
    values = list(domains[i][j])
    leastConstraingValues = sorted(values, key=lambda x: getNumLeastConstraing(x),reverse=False)
    return leastConstraingValues


def backtrackingSearch_F_B() -> bool:
    return recursiveBacktracking_F_B()


def recursiveBacktracking_F_B() -> bool:
    global nodesExpanded, zeroIndex, domains
    nodesExpanded+=1
    # print("lenZeros: ",lenZeros)
    # print(zeroIndex)
    if zeroIndex==lenZeros:
        return True
    i, j = selectUnassignedVariable_F_B()
    #print(assignment)
    for value in orderDomainValues_F_B(i, j):
        if isConsistent_F_B(i, j, value):
            #removeFromDomains(i, j, value)
            assignment[i][j]=value
            #print(assignment)
            if recursiveBacktracking_F_B():
                return True
            else:
                #assign_F(i, j, 0)
                assignment[i][j]=0
                domains = copy.deepcopy(domainsLevels[zeroIndex-1])
    zeroIndex-=1
    return False


if backtrackingSearch_F():
    print("SOLUTION FOUND!")
else:
    print("SOLUTION NOT FOUND!")
print(assignment)
print("Number of Nodes Expanded: ", nodesExpanded)

print("Run Time (B+F+H): ", time.time()-startTime)