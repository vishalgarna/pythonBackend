
import MetaTrader5 as mt5 
mt5.initialize()
if not mt5.initialize():
 print('Beta Tumhare Mt5 Initialize nhai hua ', mt5.last_error())

account = 126918041
password = "Vishalgarna@1"
server = "Exness-MT5Real7"

if not mt5.login(login=account, password=password, server=server):
 print('Ye Kya Kardiy credential Wrong de diya ', mt5.last_error())
 quit()