import MetaTrader5 as mt5

def placedOrder(orderDetails , symbol):
    print(orderDetails)

    # mt5.initialize()
    # if not mt5.initialize():
    #  print('Beta Tumhare Mt5 Initialize nhai hua ', mt5.last_error())

    # account = 182507753
    # password = "Vishalgarna@1"
    # server = "Exness-MT5Trial6"

    # if not mt5.login(login=account, password=password, server=server):
    #  print('Ye Kya Kardiy credential Wrong de diya ', mt5.last_error())
    # quit()
    # symbol = orderDetails['symbol']
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"Symbol info not found for {symbol}")
        return {"message": "Symbol info not found"}

    # Calculating SL and TP
    sl_pip_value  = 50
    tp_pip_value = 500

    symbol_tick = mt5.symbol_info_tick(symbol)
    if not symbol_tick:
        print(f"Symbol tick data not found for {symbol}")
        return {"message": "Symbol tick data not found"}

    symbol_open_price = symbol_tick.ask if orderDetails["type"] == "BUY" else symbol_tick.bid
    point = symbol_info.point

    print('point' , point)


    if orderDetails["type"] == "BUY":

        take_sl = symbol_open_price - tp_pip_value * point
        take_tp = symbol_open_price + tp_pip_value * point


    else :
        take_sl = symbol_open_price - tp_pip_value * point
        take_tp = symbol_open_price + tp_pip_value * point


    order_request = {
        'action': mt5.TRADE_ACTION_DEAL,
        'symbol': symbol,
        'volume': 0.01,  # Ensure volume is float
        'type': mt5.ORDER_TYPE_SELL if orderDetails["type"] == "SELL" else mt5.ORDER_TYPE_BUY,
        'price': symbol_open_price,
        # 'sl': take_sl,
        # 'tp': take_tp,
        'deviation': 20,
        'magic': 234000,
        'comment': "Python script order",
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_IOC,
    }

    order_result = mt5.order_send(order_request)
    if order_result is None or order_result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Failed to place order. Order result:", order_result)
        return False

    print(f"Order placed successfully: {order_result}")
    return  True




# orderDetails = { "symbol": "DXYm", "type": "BUY", "sl": 30,"tp": 50  } # 50 pips } 

# result = placedOrder(orderDetails) 
# print(result)
