"""Authors:
    Angus Boyer (46415282)
    Gunit Singh (47425704)

MATH3202 Assignment 2: Integer Programming"""

from gurobipy import *
import math

m = Model("Eradication")

#Given information from Comm 8
CCDPop = [5066,5073,3386,6435,3653,6109,4392,4110,4381,5511,3589,3325,3914,5843,5009,5064,4579,3994,3827,5663,3600,3945,3229,5133,4212]
#Possible options for Comm 10
Options = ['Option 1', 'Option 2', 'Option 3', 'Option 4']

""" SETS """
O = range(len(Options)) #Set of options
C = range(len(CCDPop)) #Set of CCDs
""" SETS """

"""DATA"""
Probs = [0.95,0.975,0.99,0.995] #Probability of each option

LProbs = [math.log(0.95,10),math.log(0.975,10),math.log(0.99,10),math.log(0.995,10)] #Log with base 10 of all probabilities

#The cost of each option at each CCD
ECost = [
[55000,113000,214000,445000],
[65000,134000,241000,465000],
[69000,135000,242000,456000],
[65000,135000,215000,410000],
[52000,128000,234000,423000],
[51000,123000,210000,472000],
[70000,128000,209000,445000],
[60000,128000,232000,431000],
[56000,138000,247000,421000],
[70000,138000,236000,421000],
[52000,115000,228000,449000],
[62000,136000,214000,474000],
[53000,139000,217000,464000],
[56000,114000,203000,477000],
[69000,133000,253000,427000],
[65000,109000,255000,477000],
[62000,136000,248000,471000],
[51000,126000,235000,455000],
[62000,104000,230000,417000],
[52000,111000,221000,404000],
[64000,124000,215000,426000],
[54000,103000,238000,424000],
[58000,138000,230000,462000],
[54000,136000,213000,472000],
[69000,123000,256000,452000]
]
 
num=1 #number of options picked for each CCD

Budget = 6825000 #the set out budget, this is tested for different values (between 1496000 (the least budget required to pick cheapest option for all CCD), and $6825000 which is the cheapest cost for getting atleast 0.8 eradication)


"""DATA"""

"""VARIABLES"""
#X[c,o] is 1 if option o in O is picked at CCD c in C, 0 else
X={}
for o in O:
    for c in C:
        X[c,o]=m.addVar(vtype=GRB.BINARY)   
  
"""VARIABLES"""

"""OBJECTIVE FUNCTION"""
#The objective is to maximise the probabiltiy of eradication at Pacific Paradise, which is same as maximises the log of probabiltiy of eradication at Pacific Paradise as log is an increasing function
m.setObjective(quicksum(LProbs[o]*X[c,o] for o in O for c in C),GRB.MAXIMIZE)

"""OBJECTIVE FUNTION"""

"""CONSTRAINTS"""
#The total cost of the operation must not exceed the set out budget
m.addConstr(quicksum(ECost[c][o]*X[c,o] for c in C for o in O)<=Budget)

# X[c,o] must add to 1 for each CCD (so that exactly 1 option picked for each CCD)
for c in C:
    m.addConstr(quicksum(X[c,o] for o in O)==num)

"""CONSTRAINTS"""
#optimize the problem
m.optimize()

#print out the pciked options for each CCD
for c in C:
    print('For CCD',c,'pick the option with probability',sum(Probs[o]*X[c,o].x for o in O))

#print out the actual cost, which could be smaller than the set out budget
print('Total cost of the operation is', sum(ECost[c][o]*X[c,o].x for c in C for o in O))
#print out the eradication probability, from the log (hence raise 10 to the power of m.objval)
print("The eradication probability at the Pacific Paradise", 10**m.objval)