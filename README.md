# manager-bot

## Описание
Настольная программа с графическим интерфейсом, которая реализует алгоритм
 round-robin

## round-robin
Популярный алгоритм распределения нагрузки между исполнителями round-robin подразумевает наличие N исполнителей
 и M задач, обычно N много меньше чем M. Алгоритм заключается в простом распределении задач по исполнителям в цикле.
  Первому исполнителю назначается первая задача, второму -- вторая и т. д. N+1 - я задача снова назначается первому исполнителю, и так далее по кругу.

Дополнительные сведения 
[round-robin (wiki)](https://ru.wikipedia.org/wiki/Round-robin_(%D0%B0%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC)


## Пример работы
![Alt Text](https://ibb.co/ka49vq)

## Требования

Для запуска программы требуется:

_Python 3.6_

## Как установить:

1. Установить Python3:

(Windows):[python.org/downloads](https://www.python.org/downloads/windows/)

(Debian):
```sh
sudo apt-get install python3
sudo apt-get install python3-pip
```
2. Установить зависимости и скачать сам проект:

```sh
git clone https://github.com/Safintim/manager_bot.git
cd manager_bot
pip3 install -r requirements.txt
```

## Как использовать: 
***
```sh
python3 manager_bot.py
```

## Комментарий
Мои впечатления и сложности реализации можно прочитать[ в моем блоге](https://waytoperfection291100265.wordpress.com/2018/10/27/25-%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82-%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80-%D0%B1%D0%BE%D1%82/)