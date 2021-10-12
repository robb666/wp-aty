
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time


def driver():
    options = Options()
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--headless')
    return webdriver.Chrome(options=options)  # koniecznie --headless przy cron


driver = driver()


url = 'https://everest.pzu.pl/pc/PolicyCenter.do'

tasks = ['Rozlicz']

personal_data = {}

location = "/run/user/1000/gvfs/smb-share:server=192.168.1.12,share=e/Agent baza/Login_Hasło.xlsx"

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

ws = pd.read_excel(location, index_col=None, na_values=['NA'], usecols="A:G")
df = pd.DataFrame(ws).head(50)

# new_header = df.iloc[1]
# df = df[3:]
# df.columns = new_header
# df = df.rename(index=lambda x: x + 2)

row_num = 30

log = df.iloc[row_num - 2, 5]
h = df.iloc[row_num - 2, 6]


driver.get(url)
driver.find_element_by_id('input_1').send_keys(log)
driver.find_element_by_id('input_2').send_keys(h)
driver.find_element_by_css_selector('.credentials_input_submit').click()
driver.find_element_by_id('Login:LoginScreen:LoginDV:username-inputEl').send_keys(log)
driver.find_element_by_id('Login:LoginScreen:LoginDV:password-inputEl').send_keys(h)
driver.find_element_by_id('Login:LoginScreen:LoginDV:submit').click()

WebDriverWait(driver, 9).until(EC.presence_of_element_located((By.XPATH,
                                                              "//*[contains(text(), 'Rozlicz')]"))).click()
kwota = WebDriverWait(driver, 9).until(EC.presence_of_element_located((By.ID,
                                                   "ProducerStatementReportOnlinePzu:0:PaymentAmount-inputEl"))).text
driver.quit()

path = '/run/user/1000/gvfs/smb-share:server=192.168.1.12,share=e/Wpłaty/inkaso.txt'

if kwota != '0':
    with open(path, 'w') as f:
        f.write(f'PZU: {kwota}')
else:
    pass

