
from __future__ import print_function
from ahk import AHK
import sys
import os
import time
import re
from L_H_ks import link, numpad

ahk = AHK()


def open_browser():
    ahk.run_script('Run, firefox.exe -new-window ' + link)
    time.sleep(9)
    for window in ahk.windows():
        if 'Santander' in window.title.decode('windows-1252'):
            win = window
            win.maximize()
            window.always_on_top = True
            return win


def log_into_account():
    ahk.mouse_move(1725, 190, speed=10)
    # ahk.run_script('ImageSearch, 1172, 94, 1625, 246, Zaloguj.png')
    ahk.click()
    ahk.mouse_move(1725, 259, speed=10)
    ahk.click()
    time.sleep(5)
    ahk.run_script(f'Send, {numpad}')
    ahk.mouse_move(1297, 428, speed=10)
    ahk.click()
    time.sleep(3)
    ahk.click()
    time.sleep(8)


def read_amount():
    file = r'M:\Wpłaty\inkaso.txt'
    if os.path.exists(file):
        with open(file, 'r') as f:
            amount = re.search(': (\d*\s?\d+,\d+)', f.read()).group(1)
        os.remove(file)
        return amount.replace(' ', '')
    else:
        sys.exit()


def transfer(win, amount):
    ahk.mouse_move(841, 219, speed=10)
    ahk.click()
    time.sleep(5)
    ahk.mouse_move(1365, 669, speed=10)
    ahk.click()
    time.sleep(2)
    ahk.mouse_move(1232, 1062, speed=10)  # wybór z listy
    ahk.click()
    time.sleep(2)
    for n in amount:
        if re.search('[0-9]', n):
            num = '{Numpad' + f'{n}' + '}'
            ahk.run_script(f"Send, {num}")
        else:
            ahk.send_input('`,')
    for _ in range(5):
        ahk.mouse_wheel('down')
    ahk.mouse_move(1386, 922, speed=10)
    ahk.click()
    time.sleep(5)
    for _ in range(5):
        ahk.mouse_wheel('down')
    ahk.mouse_move(1338, 767, speed=10)
    ahk.click()  # run
    time.sleep(5)
    win.close()
    file = r'M:\Wpłaty\dokonane wpłaty.txt'
    with open(file, 'a') as f:
        f.write(f"Wpłata do PZU w wysokości {amount} zł wykonana dnia {time.strftime('%d.%m.%Y o godzinie %H:%M')}\n")


amount = read_amount()
win = open_browser()
log_into_account()
transfer(win, amount)
