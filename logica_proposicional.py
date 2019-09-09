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
    s = s.lower()
    return s == 'p' or s == 'q' or s == 'r' or s == 's' or s == 't' or s == 'f' or None


def valid_formula(f):
    """
    Valid if the characters of the formula are part of it, positions of characters.
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
                        if f[n + 1] == ')' or (f[n - 1] == '(' and f[n] != '!'):
                            print('Formula error, "{value}" is not a valid value.'.format(
                                value=f[n] + (f[n + 1] if not sigma(f[n + 1]) else not f[n - 1])))
                            return False

                # Validate two or more values of the same type
                # Example: (pp-q) Error, (p--q) Error, (p-) Error, (p-q)s Error, s(p=q) Error
                if (sigma(f[n]) and sigma(f[n + 1])) or (symbol(f[n]) and symbol(f[n + 1]) and f[n + 1] != '!') or \
                        (f[n] == ')' and sigma(f[n + 1])) or (f[n] == '(' and sigma(f[n - 1])) or \
                        (sigma(f[n]) and symbol(f[n + 1]) and f[n + 1] == '!'):
                    m = (f[n - 1] + f[n]) if (f[n] == '(' and sigma(f[n - 1])) else f[n] + f[n + 1]
                    print('Formula error, "{value}" is not a valid value.'.format(value=m))
                    return False

            except:
                pass

        else:
            s = False
            print('Formula error, "{value}" is not a valid value.'.format(value=f[n]))

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
                print('Formula error in:', m)
                return formula
        elif f == 'sb0' or max <= 5:
            formula = ''
            print('Status: Ok, Well formed formula')
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

        s1 = f.find(v)  # Position before the sub formula

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


def __main__(f):
    print('Formula to evaluate: {formula}'.format(formula=f))
    sf = []
    _f = tour_formula(f, sf)

    if _f:
        f = assemble_sf(sf, _f)
        if len(f) > 0 and f != 'sb0' and f != _f:
            __main__(f)
        else:
            print('Status: Ok, Well formed formula')


def count_parenthesis(f):
    """
    Count parentheses of formula
    :param f: formula
    :return: True is equal or False is they are different
    """
    n = 0
    p_o = 0
    p_c = 0
    while n < len(f):
        if f[n] == '(':
            p_o += 1
        if f[n] == ')':
            p_c += 1

        n += 1

    if p_o == p_c:
        return True

    print(
        """Formula error, there is no equal number of opening and closing parentheses. \n 
        Open: {open}, Close: {close}""".format(open=p_o, close=p_c))
    return False


def capture_data():
    formula = '(!(p-q)-s)'
    n = int(input("""
            ||       |||||||
            ||       ||    ||
            ||       |||||||
            ||       ||
            |||||||  ||

            Welcome.

            Select 1 if you want to enter a new formula or 2 to evaluate default formula: [1/2] """))

    if n == 1:
        formula = input("""
            /////////////////////////////////////////////////////////////////////////////
            /////////////////////////////////////////////////////////////////////////////

            Binary Connectors:
            & = Conjunction
            | = Disjunction
            "-" = Implication
            "=" = BiConditional

            Allowed SIGMA Values: 'p, q, r, s'

            False and certainty constants respectively: 'F, T'

            Negation: '!'

            Example of formula: (!(p-q)-s)

            /////////////////////////////////////////////////////////////////////////////
            /////////////////////////////////////////////////////////////////////////////

            Enter your formula: """)

    return formula


if __name__ == '__main__':
    f = capture_data()
    if valid_formula(f) and count_parenthesis(f):
        __main__(f)
