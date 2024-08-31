'''
Approach2_max_epsilon
'''

import gurobipy as grb
import numpy as np

def Approach2_max_epsilon(x, A, AC, q, epsilon0, s, G):

    Model = grb.Model("Approach2_max_epsilon")

    n = x.shape[0]
    m = x.shape[1]

    z = np.zeros((n, m, s))
    for i in range(0, n):
        for j in range(0, m):
            if x[i, j] == G[j, s]:
                z[i, j, s - 1] = 1
            for l in range(1, s + 1):
                if x[i, j] >= G[j, l - 1] and x[i, j] < G[j, l]:
                    z[i, j, l - 1] = 1

    b = Model.addVars(range(1, q), lb=0, vtype=grb.GRB.CONTINUOUS, name="b")
    U_break = Model.addVars(range(1, m + 1), range(1, s + 2), lb=0, ub=1, vtype=grb.GRB.CONTINUOUS, name="U_break")
    u = Model.addVars(range(1, n + 1), range(1, m + 1), vtype=grb.GRB.CONTINUOUS, name="u")
    v = Model.addVars(range(1, m + 1), range(1, s + 1), lb=-10, vtype=grb.GRB.CONTINUOUS, name="v")
    global_u = Model.addVars(range(1, n + 1), vtype=grb.GRB.CONTINUOUS, name="global_u")
    epsilon = Model.addVar(lb=0, vtype=grb.GRB.CONTINUOUS, name='epsilon')

    Model.update()

    Model.setObjective(epsilon, grb.GRB.MAXIMIZE)

    Model.addConstrs(b[h + 1] - b[h] >= epsilon for h in range(1, q - 1))

    Model.addConstrs(v[j, l] == U_break[j, l + 1] - U_break[j, l] for j in range(1, m + 1) for l in range(1, s + 1))

    Model.addConstrs(u[i, j] == grb.quicksum(U_break[j, 1] * z[i - 1, j - 1, l - 1] for l in range(1, s + 1)) +
                     grb.quicksum(v[j, a] * z[i - 1, j - 1, l - 1] for l in range(2, s + 1) for a in range(1, l)) +
                     grb.quicksum((x[i - 1, j - 1] - G[j - 1, l - 1])/(G[j - 1, l] - G[j - 1, l - 1]) * v[j, l] * z[i - 1, j - 1, l - 1]
                                  for l in range(1, s + 1)) for i in range(1, n + 1) for j in range(1, m + 1))

    Model.addConstrs(global_u[i] == grb.quicksum(u[i, j] for j in range(1, m + 1)) for i in range(1, n + 1))

    Model.addConstrs(global_u[A[i - 1]] >= b[AC[i - 1] - 1] for i in range(1, len(A) + 1) if
                     AC[i - 1] != 1 and AC[i - 1] != q)
    Model.addConstrs(global_u[A[i - 1]] <= b[AC[i - 1]] - epsilon for i in range(1, len(A) + 1) if
                     AC[i - 1] != 1 and AC[i - 1] != q)

    Model.addConstrs(global_u[A[i - 1]] <= b[AC[i - 1]] - epsilon for i in range(1, len(A) + 1) if AC[i - 1] == 1)
    Model.addConstrs(global_u[A[i - 1]] >= b[AC[i - 1] - 1] for i in range(1, len(A) + 1) if AC[i - 1] == q)

    Model.addConstr(epsilon >= epsilon0)


    Model.optimize()

    adj = Model.objVal

    for var in Model.getVars():
        print(f"{var.varName}: {var.X}")

    U_break1 = np.zeros((m, s + 1))
    for j in range(1, m + 1):
        for l in range(1, s + 2):
            U_break1[j - 1, l - 1] = U_break[j, l].X

    B = [0] * (q - 1)
    for h in range(1, q):
        B[h - 1] = b[h].X

    return adj