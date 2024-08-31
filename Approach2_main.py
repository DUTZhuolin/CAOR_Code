'''
Approach2_main
'''

from Preference_adjustment import *
from Approach2_max_epsilon import *
from Approach2_min_slope import *
from Obtain_b0_bq import *
from Obtain_G import *
import scipy.io as sio

def Approach2_main(x, A, AC, q, epsilon, s, G):

    e = Consistency_check(x, A, AC, q, epsilon, s, G)
    if e > 0 :
        AC11 = Preference_adjustment(x, A, AC, q, epsilon, s, G)
    else:
        AC11 = AC

    mepsilon = Approach2_max_epsilon(x, A, AC11, q, epsilon, s, G)
    [U_break1, B, sum_gamma] = Approach2_min_slope(x, A, AC11, q, mepsilon, s, G)

    Final_B = Obtain_b0_bq(U_break1, B, mepsilon)

    return U_break1, Final_B, sum_gamma, mepsilon, AC11




if __name__ == '__main__':
    test_data = sio.loadmat(r'numerical_input_data.mat')

    x = test_data['x']
    A = test_data['A'][0]
    AC = test_data['AC'][0]

    criteria_range = min_max_criteria(x)
    q = 4
    epsilon = 0.001
    s = 4

    G = get_G(s, criteria_range)
    [U_break1, Final_B, sum_gamma, mepsilon, AC11] = Approach2_main(x, A, AC, q, epsilon, s, G)