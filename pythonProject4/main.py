from exp_root import exponentiation
from exp_root import root
from factorial import factorial
from logarithm import logarithm
import sys
def main():
    x = int(input('enter 1 if you want to use exp_root \n enter 2 if you want to use factorial \n enter 3 if you want to use logarithm: '))

    if x == 1:
        y = int(input('enter 1 if you want to use exponentiation \n enter 2 if you want to use root: '))
        if y == 1:
            z = int(input('enter 1 if you want to use exp2 \n enter 2 if you want to use exp3: '))
            if z == 1:
                exponentiation.exp2(float(input('Введіть число: ')))
            elif z == 2:
                exponentiation.exp3(float(input('Введіть число: ')))
        elif y == 2:
            l = int(input('enter 1 if you want to use root2 \n enter 2 if you want to use root3: '))
            if l == 1:
                root.root2(float(input('Введіть число: ')))
            elif l == 2:
                root.root3(float(input('Введіть число: ')))
    elif x == 2:
        factorial.fact(float(input('Введіть число: ')))
    elif x == 3:
        m = int(input('enter 1 if you want to use log \n enter 2 if you want to use ln \n enter 3 if you want to use lg: '))
        if m == 1:
            logarithm.log(float(input('Введіть основу: ')),float(input('Введіть число: ')))
        elif m == 2:
            logarithm.ln(float(input('Введіть число: ')))
        elif m == 3:
            logarithm.lg(float(input('Введіть число: ')))
    while True:
        res = input('Запустити програму заново? ')
        if res == 'Так':
            main()
        else:
            sys.exit(0)

if __name__ == '__main__':
    main()