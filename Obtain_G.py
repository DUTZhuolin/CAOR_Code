import numpy as np

def min_max_criteria(x):
    m = x.shape[1]
    criteria_range = np.zeros((m, 2))
    for j in range(0, m):
        criteria_range[j, 0] = min(x[:, j])
        criteria_range[j, 1] = max(x[:, j])
    return criteria_range


def get_G(s, criteria_range):
    m = criteria_range.shape[0]
    G = np.zeros((m, s + 1))

    for j in range(0, m):
        for l in range(0, s + 1):
            if l == 0:
                G[j, l] = criteria_range[j, 0]
            elif l == s:
                G[j, l] = criteria_range[j, 1]
            else:
                G[j, l] = G[j, l-1] + (criteria_range[j, 1] - criteria_range[j, 0])/s
    return G