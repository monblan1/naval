import math

print('Стр.124 номер 2')
a = [int(input()), int(input()), int(input())]
print(f'{a[0]} + {a[1]} + {a[2]} = {a[0] + a[1] + a[2]}\n'
      f'{a[0]} * {a[1]} * {a[2]} = {a[0] * a[1] * a[2]}\n'
      f'({a[0]} + {a[1]} + {a[2]})/3 = {(a[0] + a[1] + a[2]) / 3}\n')

print('Стр.124 номер 3')
r = float(input())
print(f'Длина окружности: {2 * math.pi * r}\n'
      f'Площадь круга: {math.pi * (r ** 2)}')

print('Стр.124 номер 4')
x = int(input())
y = int(input())
print(f'До: {x}, {y}')
x, y = y, x
print(f'После: {x}, {y}')
