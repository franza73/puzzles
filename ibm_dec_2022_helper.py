def hash_to_box(s):
    h, first, second = s.split()
    LH = len(h)
    if LH == 12:
        N = 4
    elif LH == 15:
        N = 5
    elif LH == 20:
        N = 5
    elif LH == 21:
        N = 7
    elif LH == 22:
        N = 11
    else:
        print('ERROR: Unexpected hash length')
        exit(1)
    H = {}
    for i in range(LH):
        H[h[i]] = i % N
    s = first + second[1:]
    LS = len(s)
    while True:
        cnt = 0
        for i in range(1, LS):
            if H[s[i]] == H[s[i-1]]:
                for j in range(i+1, LS):
                    if H[s[j]] != H[s[i]]:
                        H[s[j]], H[s[i]] = H[s[i]], H[s[j]]
                        break
            else:
                cnt += 1
        if cnt == LS - 1:
            break
    L = [''] * N
    for x, y in sorted([(b, a) for a, b in H.items()]):
        L[x] += y
    return f'{L} {first} {second}'


if __name__ == "__main__":
    s15 = 'acefgiknqrstuvx kafkaesque extravagancies'
    s12 = 'acefknopqsux kafkaesque exponence'
    s20 = 'abcdeghiklnopqrstuvy triskaidekaphobe equivocatingly'
    s21 = 'abceghijklnopqrstuvwy blepharoconjunctivitis squawkingly'
    s22 = 'abcdeghijlmnoprstuvxyz blepharoconjunctivitis semioxygenized'
    print(hash_to_box(s12))
    print(hash_to_box(s15))
    print(hash_to_box(s20))
    print(hash_to_box(s21))
    print(hash_to_box(s22))
