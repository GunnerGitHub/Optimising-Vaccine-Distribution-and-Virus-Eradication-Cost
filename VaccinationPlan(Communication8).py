"""Authors:
    Angus Boyer (46415282)
    Gunit Singh (47425704)

MATH3202 Assignment 2: Integer Programming"""

from gurobipy import *

m = Model("Vaccination Distribution")

""" Data Provided """
IDtoLVC = [
[59.1,15.3,91.7,73.0,61.8,61.8,5.3,16.8],
[90.2,45.4,60.4,39.8,6.0,65.4,63.2,66.8],
[38.6,58.2,39.7,37.2,62.7,5.5,72.4,56.0]
]

CCDPop = [5066,5073,3386,6435,3653,6109,4392,4110,4381,5511,3589,3325,3914,5843,5009,5064,4579,3994,3827,5663,3600,3945,3229,5133,4212]

CCDtoLVC = [
[0,27.1,0,0,0,0,7.5,25.0],
[0,20.1,0,0,0,0,19.1,0],
[0,18.6,0,0,0,0,32.1,0],
[0,41.5,0,0,11.3,0,0,0],
[0,0,0,47.6,16.1,0,0,0],
[0,20.2,0,0,0,0,10.5,10.3],
[0,10.8,0,0,0,0,11.6,14.3],
[0,14.3,0,0,32.5,0,0,0],
[0,34.5,0,0,12.2,0,0,0],
[0,0,0,26.8,9.2,0,0,0],
[31.5,0,0,0,0,0,0,15.9],
[0,23.2,0,0,0,0,29.8,12.4],
[0,0,0,29.3,0,21.5,0,0],
[0,0,0,18.1,30.9,30.5,0,0],
[0,0,0,15.5,21.6,0,0,0],
[11.7,0,0,0,0,0,0,31.2],
[17.8,0,0,0,0,23.2,0,0],
[0,0,0,28.4,0,10.3,0,0],
[0,0,18.7,16.0,0,26.2,0,0],
[0,0,8.4,14.6,0,0,0,0],
[15.8,0,0,0,0,42.8,0,0],
[26.1,0,0,0,0,19.9,0,0],
[0,0,39.3,0,0,19.3,0,0],
[0,0,25.9,31.1,0,21.0,0,0],
[0,0,6.3,23.9,0,0,0,0]
]
LVCUCost = [1397000,1591000,1384000,1167000,1530000,1921000,1791000,1001000]

ES = [4138000,3735000,5503000,3535000,4400000,5513000,4115000,5113000]

""" Data Provided """

""" SETS """
Depots = ["ID-A (0)", "ID-B (1)", "ID-C(2)"]
V = range(len(Depots))

LocalCentre = ["LVC0","LVC1","LVC2","LVC3",
               "LVC4","LVC5","LVC6","LVC7"]
L = range(len(LocalCentre))

#A[i,j] gives the distance (km) from Id i to LVC l
A = {}
for n in range(len(Depots)):
    for c in range(len(IDtoLVC[n])):
        A[(n,c)] = IDtoLVC[n][c]
        

#B[i,j] gives the distance (km) from CDD c to LVC l
B= {}
for n in range(len(CCDtoLVC)):
    for c in range(len(CCDtoLVC[n])):
        B[(n,c)] = CCDtoLVC[n][c]

C = range(len(CCDPop))

""" SETS """

""" DATA """

icost = [144,105,157] #importation costs

pop = CCDPop #population of CCDs

l1 = A #length of arc A

l2 = B #length of arc B

costIL = 0.2 #cost/km tavel for arc A

costCL = 1 #cost/km tavel for arc B

maxID = 46000 #max capacity at each ID

upgrade = LVCUCost

closing = ES

initialLVC= 13000 #capacity of LVC (without upgrade)

increase = 0.5 #increase in capacity if LVC upgraded

num = 1 #number of LVC's a CCD can be asigned to

""" DATA """

""" VARIABLES """
#no. of vaccines flowing through A
X = {}
for a in A:
    X[a] = m.addVar()

#no. of vaccines flowing through B
Y = {}
for b in B:
    Y[b] = m.addVar()

#Binary variable represents 1 for upgrade of LVC, 0 else
S={}
for l in L:
    S[l]= m.addVar(vtype=GRB.BINARY)

#Binary variable represents 1 for closure of LVC, 0 else
CL ={}
for l in L:
    CL[l]= m.addVar(vtype=GRB.BINARY)
    
#Binary variables reprsetns 1 for a CCD assigned to particular LVC, 0 if not
LC ={}
for b in B:
    LC[b]=m.addVar(vtype=GRB.BINARY)

""" VARIABLES """

""" OBJECTIVE FUNCTION """
m.setObjective(quicksum(icost[v]*X[a] for v in V for a in A if a[0]==v) 
               +quicksum(l1[a]*costIL*X[a] for a in A)
               +quicksum(l2[b]*costCL*Y[b] for b in B)
               +quicksum(upgrade[l]*S[l] for l in L)
               -quicksum(closing[l]*CL[l] for l in L),
               GRB.MINIMIZE)
""" OBJECTIVE FUNCTION """

""" CONSTRAINTS """

#the total amount of vaccines going to a CCD from its neighbouring assigned LVC must be equivalent to the population of the CCD.
for c in C:
    m.addConstr(quicksum(LC[b]*Y[b] for b in B if b[0]==c)==pop[c])

#the demand of vaccines at an LVC, as the vaccines flowing out of it in a week must be equivalent to those flowing into it.
#Note, no vaccines flow from LVC if it is closed
for l in L:
    m.addConstr(quicksum((1-CL[l])*X[a] for a in A if a[1]==l) 
                    == quicksum(Y[b] for b in B if b[1]==l)) #note B has opposite key 
        
#the citizens of CCD’s are only able to obtain the vaccine from a neighbouring LVC (as a distance of 0km in the data represents a non-neighbouring LVC).
for b in B:
    if B[b]==0:
        m.addConstr(Y[b]==0)

#Vaccines imported at ID's must be less than its capacity through the whole operation
for v in V:
    m.addConstr(quicksum(X[a] for a in A if a[0]==v)<=maxID)

#Vaccines administered at LVC must be less than its capacity (account for possible upgrade) throguh the whole operation
for l in L:
    m.addConstr(quicksum(X[a] for a in A if a[1] == l)<=initialLVC*(1+increase*S[l]))
    
#each CCD must only be assigned to one LVC
for c in C:
    m.addConstr(quicksum(LC[b] for b in B if b[0]==c)==num)

""" CONSTRAINTS """

""" OPTIMISE and FINAL ANSWER """
m.optimize()

print("Total vaccines produced in the operation was",sum(X[a].x for a in A))
    
print("Total cost of the operation is", m.objval)

""" OPTIMISE and FINAL ANSWER """

