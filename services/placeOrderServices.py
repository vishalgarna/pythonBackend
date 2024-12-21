import MetaTrader5 as mt5


def placedOrder(orderDetails):
    print(orderDetails)

    if not mt5.symbol_select(orderDetails['symbol']):
        print('le lo ladu aur dalo galat symbol ', orderDetails['symbol'])
        return {"message": "Invalid symbol"}

    symbol = orderDetails['symbol']
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"Symbol info not found for {symbol}")
        return {"message": "Symbol info not found"}

    order_request = {
        'action': mt5.TRADE_ACTION_DEAL,
        'symbol': symbol,
        'volume': 0.1,  # Ensure volume is float
        'type': mt5.ORDER_TYPE_SELL if orderDetails["type"] == "SELL" else mt5.ORDER_TYPE_BUY,
        'price': symbol_info.bid if orderDetails["type"] == "SELL" else symbol_info.ask,
        "sl" : orderDetails["sl"],
        "tp" : orderDetails["tp"],
        'deviation': 20,
        'magic': 234000,
        'comment': "Python script order",
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_IOC,
    }

    order_Result = mt5.order_send(order_request)
    if order_Result is None:
        print("Failed to place order. Order result is None.") 
        return False
    else :
        return True
    