def symbol(s):
    return s == '!' or s == '&' or s == '|' or s == '=' or s == '==' or None


def sigma(s):
    return s == 'p' or s == 'q' or s == 'r' or s == 's' or None


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


def tour_formula(formula, sf):
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
        elif sigma(f[n]) or f == 'sb0' or symbol(f[n]) and f[n + 1] + f[n + 2] == 'sb' and max <= 4:
            formula = ''
            print('Formula bien formada')
            return formula
        elif not sigma(f[n]):
            formula = ''
            print('Error de formula, valor "{valor}" no pertenece a sigma.'.format(valor=f[n]))
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


def valid_sf(f):
    n = 0
    s = True
    m = len(f)
    while n < m:
        if symbol(f[n]) or sigma(f[n]) or f[n] == '(' or f[n] == ')':
            pass
        else:
            s = False
            print('Error de formula, "{valor}" no es un valor válido.'.format(valor=f[n]))

        n += 1

    return s


def reuse(f, sf):
    sf = []
    _f = f
    _f = tour_formula(_f, sf)
    if _f:
        f = assemble_sf(sf, _f)
        if len(f) > 0:
            reuse(f, sf)


def __main__():
    formula = '(pp|u)'
    sf = []
    j = valid_sf(formula)
    if j:
        tour_formula(formula, sf)
        _f = formula
        f = assemble_sf(sf, _f)

        if len(f) > 0 and f != 'sb0' and f != formula:
            reuse(f, sf)


if __name__ == '__main__':
    __main__()
