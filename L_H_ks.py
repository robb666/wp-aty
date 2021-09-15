
from openpyxl import load_workbook

wb = load_workbook(filename="M:\Agent baza\Login_Hasło.xlsx", read_only=True)
ws = wb['Arkusz1']

numpad = '{Numpad1}{Numpad3}{Numpad9}{Numpad2}{Numpad1}{Numpad9}{Numpad0}{Numpad0}'

link = 'https://www.santander.pl/klient-indywidualny'
