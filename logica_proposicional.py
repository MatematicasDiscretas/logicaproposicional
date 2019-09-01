def symbol(s):
    return s == '!' or s == '&' or s == '|' or s == '=' or s == '==' or None


def extract_sub_formula(n, m, f, sf):
    key = 'sb' + str(n)
    sub = {key: '('}
    q = n

    while q < m:
        try:
            if f[q + 1] and f[q + 1] != ')':
                sub[key] = sub[key] + f[q + 1]
            else:
                sub[key] = sub[key] + ')'
                sf.append(sub)
                return n
        except:
            pass
        q += 1


def tour_formula(signature, formula, sf):
    f = formula
    n = 0
    max = len(f)
    while n < max:
        if f[n] == '(' and f[n + 1] != '(':
            if f.find(')', n) != -1:
                n = extract_sub_formula(n, max, f, sf)
            else:
                formula = ''
                m = ''
                for x in range(n, max):
                    m += f[x]
                print('Error de formula en : ', m)
                return formula
        elif f == 'sb0' or symbol(f[n]) and f[n + 1] + f[n + 2] == 'sb' and max <= 4:
            formula = ''
            print('Formula bien formada')
            return formula

        n += 1

    return formula


def assemble_sf(sf, f):
    n = 0
    max = len(sf)
    while n < max:
        r = sf[n]
        k = list(r.keys())[0]
        v = sf[n][k]

        s1 = f.find(v)  # Posición antes de la sub formula

        # Exist binary symbol
        try:
            if symbol(f[s1 - 1]) and symbol(f[s1 + len(v)]):
                k = '(' + k
                if max == 1:
                    f = f + ')'
            elif symbol(f[s1 - 1]) and f[s1 + len(v)] != ')' and not symbol(f[s1 + len(v)]):
                k = k + ')'
        except:
            pass

        f = f.replace(v, k)
        n += 1

    return f


def reuse(s, f, sf):
    sf = []
    _f = f
    _f = tour_formula(s, _f, sf)
    if _f:
        f = assemble_sf(sf, _f)
        print('F: ', f)
        if len(f) > 0:
            reuse(s, f, sf)


def __main__():
    signature = ['p', 'q', 'r', 's']
    formula = '(p&q)'
    sf = []
    tour_formula(signature, formula, sf)
    _f = formula
    f = assemble_sf(sf, _f)

    if len(f) > 0:
        reuse(signature, f, sf)


if __name__ == '__main__':
    __main__()
