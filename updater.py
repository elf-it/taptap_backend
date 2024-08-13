from db.db import Connection
import time

def update_coins():
    t = time.time()
    t = int(t)
    t = t + (6 * 60 * 60)
    
    connection = Connection()

    connection.update("flags", ["next_time"], [t], 2)

    connection.update("flags", ["value"], [True], 1)

    connection.disconnect()
    
    time.sleep(5)

    connection = Connection()

    cicle = connection.select("flags", "key", "cicle")
    num_value = int(cicle[0][3]) + 1
    if num_value > 3:
        num_value = 0
    print(num_value)
    connection.update("flags", ["num_value"], [num_value], 2)

    num_value = str(num_value)

    upd1 = "UPDATE coins SET end_of_day_autoclick=tarif_autoclick+1 WHERE flag_autoclick = " + num_value + " AND autoclick = true;"
    connection.updateFromStr(upd1)

    upd4 = "UPDATE coins SET my_coins_max=status, auto_coins_max=status;"
    connection.updateFromStr(upd4)
    
    upd45 = "UPDATE coins SET my_coins_max=status*coins_unlimit, auto_coins_max=status*coins_unlimit WHERE unlimit = true;"
    connection.updateFromStr(upd45)

    upd46 = "UPDATE coins SET my_coins_max=status+(status/100*coins_boost), auto_coins_max=status+(status/100*coins_boost) WHERE end_of_day_boost > 0 AND boost = true;"
    connection.updateFromStr(upd46)
    
    upd46 = "UPDATE coins SET my_coins_max=(status*coins_unlimit)+(status*coins_unlimit)/100*coins_boost, auto_coins_max=(status*coins_unlimit)+(status*coins_unlimit)/100*coins_boost WHERE end_of_day_boost > 0 AND boost = true AND unlimit = true;"
    connection.updateFromStr(upd46)
    
    upd5 = "UPDATE coins SET end_of_day_autoclick=end_of_day_autoclick-1 WHERE end_of_day_autoclick > 0 AND flag_autoclick <> " + num_value + ";"
    connection.updateFromStr(upd5)

    upd7 = "UPDATE coins SET end_of_day_boost=end_of_day_boost-1 WHERE end_of_day_boost > 0;"
    connection.updateFromStr(upd7)

    upd7 = "UPDATE coins SET boost=false, flag_boost=0, coins_boost=0, end_of_day_boost=0, tarif_boost=0 WHERE end_of_day_boost = 0;"
    connection.updateFromStr(upd7)

    #--------------------

    connection.disconnect()
    
    time.sleep(5)

    connection = Connection()

    connection.update("flags", ["value"], [False], 1)

    connection.disconnect()

update_coins()