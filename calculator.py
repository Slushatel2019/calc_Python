from math import pow

def get_prior(sign):
    if sign in ('+', '-'):
        return 2
    if sign in ('*', '/'):
        return 3
    if sign == '^':
        return 4


def prior(sign1, sign2):
    if get_prior(sign1) > get_prior(sign2):
        return 'bigger'
    if get_prior(sign1) == get_prior(sign2):
        return 'equal'
    return False


def rewrite(a):
    operators = []
    numbers = []
    c = ''
    for i in range(len(a)):
        if a[i].isnumeric():
            c += a[i]
            if i + 1 == len(a):
                numbers.append(c)
                for _ in range(len(operators)):
                    numbers.append(operators.pop())
        else:
            if c:
                numbers.append(c)
                c = ''
            if not operators:
                operators.append(a[i])
                c = ''
                continue
            if operators[-1] == '(':
                operators.append(a[i])
                c = ''
                continue
            if a[i] == '(':
                operators.append(a[i])
                c = ''
                continue
            if a[i] == ')':
                while operators[-1] != '(':
                    numbers.append(operators.pop())
                operators.pop()
                if i + 1 == len(a):
                    for _ in range(len(operators)):
                        numbers.append(operators.pop())
                c = ''
                continue
            if prior(a[i], operators[-1]) == 'bigger':
                operators.append(a[i])
                c = ''
                continue
            if prior(a[i], operators[-1]) == 'equal':
                numbers.append(operators.pop())
                operators.append(a[i])
                c = ''
                continue
            if prior(operators[-1], a[i]) == 'bigger':
                while operators and operators[-1] != '(' and prior(operators[-1], a[i]) == 'bigger':
                    numbers.append(operators.pop())
                if not operators:
                    operators.append(a[i])
                    c = ''
                    continue
                if operators[-1] == '(':
                    operators.append(a[i])
                    c = ''
                    continue
                if a[i] == '(':
                    operators.append(a[i])
                    c = ''
                    continue
                if a[i] == ')':
                    while operators[-1] != '(':
                        numbers.append(operators.pop())
                    operators.pop()
                    if i + 1 == len(a):
                        for _ in range(len(operators)):
                            numbers.append(operators.pop())
                    c = ''
                    continue
                if prior(a[i], operators[-1]) == 'bigger':
                    operators.append(a[i])
                    c = ''
                    continue
                if prior(a[i], operators[-1]) == 'equal':
                    numbers.append(operators.pop())
                    operators.append(a[i])
                    c = ''
                    continue
    return numbers


def _calc(line):
    my_stack = []
    for i in range(0, len(line)):
        n = line[i]
        if n.isnumeric():
            my_stack.append(n)
        else:
            if n == '^':
                c = pow(float(my_stack.pop(-2)), float(my_stack.pop(-1)))
            else:
                c = eval("{}{}{}".format(my_stack.pop(-2), n, my_stack.pop(-1)))
            my_stack.append(c)
    return my_stack[0]

def command_pars(text):
    if "/exit" in text:
        print('Bye!')
        return False
    if "/help" in text:
        print('The program calculates the sum and not the sum of numbers')
        return True
    print('Unknown command')
    return True

def store_value(id_value_list=[], get=False, dict_={}):
    if id_value_list:
        dict_[id_value_list[0]] = id_value_list[1]
    if get:
        return dict_

def get_value(ident):
    check_value = store_value(get=True).get(ident, False)
    if check_value:
        return check_value
    return 'Unknown variable'

def pars_equal_sign(elem):
    elem = elem.split('=', 1)
    if not elem[0].isalpha():
        print('Invalid identifier')
        return True
    if not elem[1].isnumeric() and elem[1].isalpha():
        check_value = store_value(get=True).get(elem[1], False)
        if check_value:
            store_value([elem[0], check_value])
            return True
        else:
            print('Unknown variable')
            return True
    if elem[1][0] == '-' and elem[1][1:].isnumeric():
        store_value(elem)
        return True
    if not elem[1].isnumeric():
        print('Invalid assignment')
        return True
    store_value(elem)
    return True


def pars_str(str_):
    str_ = ''.join(str_)
    line = []
    count_minus = 1
    alpha = ''
    for i in range(len(str_)):
        if str_[i].isalpha():
            if i == len(str_) - 1:
                alpha = alpha if alpha else str_[i]
            else:
                if str_[i+1].isalpha():
                    alpha += str_[i]
                    continue
            alpha = alpha if alpha else str_[i]
            check_value = store_value(get=True).get(alpha, False)
            if check_value:
                line.append(check_value)
                alpha = ''
                continue
            else:
                print('Unknown variable')
                return False
        if str_[i].isnumeric():
            line.append(str_[i])
            continue
        if str_[i] == '+':
            if str_[i+1] == '+':
                continue
            line.append(str_[i])
            continue
        if str_[i] == '-':
            if str_[i+1] == '-':
                count_minus += 1
                continue
            if count_minus % 2 == 0:
                line.append('+')
                count_minus = 1
                continue
            else:
                line.append('-')
                count_minus = 1
                continue
        else:
            line.append(str_[i])
            continue
    return ''.join(line)


while True:
    one = str(input())
    one = one.split()
    if len(one) == 1:
        if "/" in one[0]:
            if command_pars(one[0]):
                continue
            break
        if one[0].isalpha():
            print(get_value(one[0]))
            continue
        elif one[0].isnumeric():
            print(one[0])
            continue
        elif one[0][0] == '-' and one[0][1:].isnumeric():
            print(one[0])
            continue
        elif '=' in one[0]:
            pars_equal_sign(one[0])
            continue
        try:
            if not pars_str(one[0]):
                continue
            print(int(_calc(rewrite(pars_str(one[0])))))
            continue
        except:
            print('Invalid expression')
    elif len(one) == 0:
        continue
    if '=' in one:
        pars_equal_sign(''.join(one))
    else:
        try:
            print(int(_calc(rewrite(pars_str(one)))))
            continue
        except:
            print('Invalid expression')
