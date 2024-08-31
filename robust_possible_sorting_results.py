from robust_max_epsilon import *
from Obtain_G import *
import scipy.io as sio

def cal_possible_sorting(x, A, AC, q, s, G):
    x_index = [i for i in range(1, x.shape[0] + 1)]
    N_A = [ele for ele in x_index if ele not in A]
    possible_sorting = np.empty(len(N_A), dtype=object)
    r = 0
    for i in N_A:
        tem_A = A.copy()
        tem_A.append(i)
        possible_sorting[r] = []
        for h in range(1, q + 1):
            tem_AC = AC.copy()
            tem_AC.append(h)

            adj = robust_max_epsilon(x, tem_A, tem_AC, q, s, G)

            if adj > 0:
                possible_sorting[r].append(h)
        r += 1
    return possible_sorting




if __name__ == '__main__':
    test_data = sio.loadmat(r'numerical_input_data.mat')
    x = test_data['x']
    A = list(test_data['A'][0])
    AC = list(test_data['AC'][0])

    criteria_range = min_max_criteria(x)
    q = 4
    s = 4
    G = get_G(s, criteria_range)

    possible_sorting = cal_possible_sorting(x, A, AC, q, s, G)