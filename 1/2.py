from datetime import datetime

print('Стр. 132 номер 3')
n = int(input())
if n <= 0:
    n *= -1
if len(str(n)) == 3:
    print('Число трехзначное')
else:
    print('Число не трехзначное')

print('Стр. 132 номер 4')
while True:
    k = int(input('месяц>>'))
    if 1 <= k <= 12:
        if 1 <= k <= 2 or k == 12:
            print('Зима')
        elif 3 <= k <= 5:
            print('Весна')
        elif 6 <= k <= 8:
            print('Лето')
        else:
            print('Осень')
        break
    else:
        print('Такого месяца в году несуществует')

print('Стр. 132 номер 7')
while True:
    y = datetime.now().year  # год текущий
    try:  # проверка на верность даты + вычисление
        m = int(input('месяц>>'))
        d = int(input('день>>'))
        start_date = datetime(y, m, d)  # дата отсчитываемого дня
        end_date = datetime(y, 12, 31)  # конечная дата
    except ValueError as err:  # вывод ошибки если дата неверная
        print('Неверная дата')
    else:  # прекращение цикла если дата верная
        break
print((end_date - start_date).days)  # вывод ответа в днях
