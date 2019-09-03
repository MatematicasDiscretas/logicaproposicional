def symbol(s):
    """
    Check Binary Connectors or operators of the formula
    ! = Negation
    & = Conjunction
    | = Disjunction
    "-" = Implication
    "=" = BiConditional
    :param s: param connector
    :return: connector or None if not exist
    """
    return s == '!' or s == '&' or s == '|' or s == '-' or s == '=' or None


def sigma(s):
    """
    Values of formula At
    :param s: value of formula At
    :return: value of At or None
    """
    return s == 'p' or s == 'q' or s == 'r' or s == 's' or s == 'T' or s == 'V' or None


def valid_formula(f):
    """
    Valid if the characters of the formula are part of it
    :param f: formula
    :return: True if formula valid or False if not
    """
    n = 0
    s = True
    m = len(f)
    while n < m:
        if symbol(f[n]) or sigma(f[n]) or f[n] == '(' or f[n] == ')':
            try:
                # Check position of Binary Connectors or operators of the formula
                if n > 0 and f[n] != '(' and f[n] != ')' and symbol(f[n]):
                    # Forward or backward of a connector there can only be one value of At
                    # Example: (p=&) Error, or p-) Error, (p-q), True
                    if not sigma(f[n + 1]) or not sigma(f[n - 1]):
                        if f[n + 1] == ')' or f[n - 1] == '(':
                            print('Error de formula, "{valor}" no es un valor válido.'.format(
                                valor=f[n] + (f[n + 1] if not sigma(f[n + 1]) else not f[n - 1])))
                            return False

                # Validate two or more values of the same type
                # Example: (pp-q) Error, (p--q) Error
                if (sigma(f[n]) and sigma(f[n + 1])) or (symbol(f[n]) and symbol(f[n + 1])):
                    print('Error de formula, "{valor}" no es un valor válido.'.format(valor=f[n] + f[n + 1]))
                    return False

            except:
                pass

        else:
            s = False
            print('Error de formula, "{valor}" no es un valor válido.'.format(valor=f[n]))

        n += 1

    return s


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
        elif f == 'sb0' or max <= 5:
            formula = ''
            print('Formula bien formada')
            return formula
        # elif not sigma(f[n]):
        #     formula = ''
        #     print('Error de formula, valor "{valor}" no pertenece a sigma.'.format(valor=f[n]))
        #     return formula

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


def reuse(f):
    sf = []
    _f = tour_formula(f, sf)
    if _f:
        f = assemble_sf(sf, _f)
        if len(f) > 0 and f != 'sb0' and f != _f:
            reuse(f)
        else:
            print('Formula bien formada')


def __main__():
    f = '((p-q)-s))'
    v = valid_formula(f)
    sf = []
    if v:
        tour_formula(f, sf)
        _f = assemble_sf(sf, f)

        if len(_f) > 0 and _f != 'sb0' and f != _f:
            reuse(_f)


if __name__ == '__main__':
    __main__()
