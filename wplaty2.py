
from __future__ import print_function
import sys
import os
from ahk import AHK
import pyautogui
import time
import re
from L_H_ks import bnk, link, numpad


ahk = AHK()


def open_browser():
    ahk.run_script('Run, firefox.exe -new-window ' + link)
    time.sleep(20)
    for window in ahk.windows():
        if bnk in window.title.decode('windows-1252'):
            win = window
            win.maximize()
            window.always_on_top = True
            return win


def log_into_account():
    path = r'C:\Users\ROBERT\Desktop\IT\PYTHON\PYTHON 37 PROJEKTY\wpłaty\images\\'
    if pyautogui.locateOnScreen(path + r'zalog_b.png'):
        pyautogui.click(path + r'zalog_b.png')
    else:
        pyautogui.locateOnScreen(path + r'zalog_sz.png')
        pyautogui.click(path + r'zalog_sz.png')

    pyautogui.locateOnScreen(path + r'sant_int.png')
    pyautogui.click(path + r'sant_int.png')

    time.sleep(5)
    ahk.run_script(f'Send, {numpad}')
    ahk.mouse_move(1297, 428, speed=10)
    ahk.click()
    time.sleep(4)
    ahk.click()
    time.sleep(9)


def read_amount(payment_file):
    inkaso = r'M:\Wpłaty\inkaso.txt'
    if os.path.exists(inkaso):
        with open(inkaso, 'r') as f:
            amount = re.search(': (\d*\s?\d+,\d+)', f.read()).group(1)
        os.remove(inkaso)
        return amount.replace(' ', '')
    else:
        with open(payment_file, 'a') as f:
            f.write(
                f"W dniu {time.strftime('%d.%m.%Y o godzinie %H:%M')} brak należności dla PZU.\n")
        sys.exit()


def transfer(win, payment_file, amount):
    ahk.mouse_move(841, 219, speed=10)
    ahk.click()
    time.sleep(6)
    ahk.mouse_move(1365, 669, speed=10)
    ahk.click()
    time.sleep(3)
    ahk.mouse_move(1232, 1062, speed=10)  # wybór z listy
    ahk.click()
    time.sleep(3)
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
    time.sleep(6)
    for _ in range(5):
        ahk.mouse_wheel('down')
    ahk.mouse_move(1338, 767, speed=10)
    ahk.click()  # run
    time.sleep(6)
    win.close()
    with open(payment_file, 'a') as f:
        f.write(f"Wpłata do PZU w wysokości {amount} zł wykonana dnia {time.strftime('%d.%m.%Y o godzinie %H:%M')}\n")


payment_file = r'M:\Wpłaty\dokonane wpłaty.txt'
amount = read_amount(payment_file)
win = open_browser()
log_into_account()
transfer(win, payment_file, amount)
