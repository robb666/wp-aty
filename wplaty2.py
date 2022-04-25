
from __future__ import print_function
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from L_H_ks import link, san_l, san_h
sys.path.append(r"C:\Users\PipBoy3000\Desktop\IT\projekty\accounting")
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from faktury_GmailAPI import zsanpl


def read_amount(payment_file):
    inkaso = r'\\Js\e\Wpłaty\inkaso.txt'
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


def driver_prefs():
    options = webdriver.ChromeOptions()
    preferences = {'download.default_directory': r'C:\Users\PipBoy3000\Desktop\\'}
    options.add_experimental_option("prefs", preferences)

    driver = webdriver.Chrome(executable_path=r'\\Js\e\zzzProjekty\drivery przegądarek\chromedriver.exe',
                              options=options)
    return driver


def sanlog(driver, url):
    driver.get(url)
    time.sleep(1)
    try:
        driver.find_element_by_id('privacy-prompt-controls-button-accept').click()
    except:
        pass
    driver.find_element_by_xpath('//span[contains(text(), "Zaloguj")]').click()
    time.sleep(1)
    WebDriverWait(driver, 9).until(EC.presence_of_element_located((
        By.XPATH, '//a[(@title="Santander internet" and @class="button primary small")]'))).click()
    WebDriverWait(driver, 15).until(EC.url_changes(url))
    try:
        driver.find_element_by_xpath('//div[contains(text(), "Akceptuję")]').click()
    except:
        pass

    login = driver.find_element_by_id('input_nik')
    login.send_keys(san_l)
    time.sleep(2)
    try:
        WebDriverWait(driver, 9).until(EC.presence_of_element_located((By.XPATH, "//input[@id='okBtn2']"))).click()
    except:
        WebDriverWait(driver, 9).until(EC.presence_of_element_located((By.XPATH, "//input[@id='okBtn2']"))).click()
    time.sleep(2)
    btn = driver.find_element_by_id('okBtn2')
    time.sleep(1)
    btn.click()
    time.sleep(2)

    pwd = driver.find_element_by_id('ordinarypin')
    pwd.send_keys(san_h)
    driver.find_element_by_id('okBtn2').click()

    onet = driver.find_element_by_id('back-button')
    onet.click()

    time.sleep(5.5)
    tiktok = zsanpl()
    driver.find_element_by_id('input_nik').send_keys(tiktok)

    driver.find_element_by_id('okBtn2').click()


def santrans(driver, amount):
    WebDriverWait(driver, 9).until(EC.presence_of_element_located((By.ID, 'menu_transfers'))).click()
    WebDriverWait(driver, 9).until(EC.presence_of_element_located((
                                            By.XPATH, '//input[starts-with(@id, "name")][2]'))).send_keys('PZU')
    time.sleep(1)
    WebDriverWait(driver, 9).until(EC.presence_of_element_located((
                                            By.XPATH, '//*[@id="body"]/div[7]/ul/li[3]'))).click()
    WebDriverWait(driver, 9).until(EC.presence_of_element_located((
                                            By.XPATH, '//input[starts-with(@id, "creditedAmount")]'))).send_keys(amount)
    WebDriverWait(driver, 9).until(EC.presence_of_element_located((
                                            By.XPATH, '//input[@value="Dalej"]'))).click()
    time.sleep(2)
    WebDriverWait(driver, 9).until(EC.presence_of_element_located((
                                            By.XPATH, '//input[@value="Wyślij przelew"]'))).click()

    with open(payment_file, 'a') as f:
        f.write(f"Wpłata do PZU w wysokości {amount} zł wykonana dnia {time.strftime('%d.%m.%Y o godzinie %H:%M')}\n")

    time.sleep(4)
    driver.quit()


if __name__ == '__main__':
    payment_file = r'\\Js\e\Wpłaty\dokonane wpłaty.txt'
    amount = read_amount(payment_file)
    url = link
    driver = driver_prefs()
    sanlog(driver, url)
    santrans(driver, amount)
