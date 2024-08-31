
def Obtain_b0_bq(U_break1, B, max_epsilon):
    m = U_break1.shape[0]
    min_U_beeak1 = [0] * m
    max_U_beeak1 = [0] * m
    for j in range(0, m):
        max_U_beeak1[j] = max(U_break1[j, :])
        min_U_beeak1[j] = min(U_break1[j, :])

    q = len(B) + 1
    Final_B = [0] * (q + 1)
    Final_B[0] = sum(min_U_beeak1)
    Final_B[q] = sum(max_U_beeak1) + max_epsilon

    for h in range(1, q):
        Final_B[h] = B[h - 1]

    return Final_B

