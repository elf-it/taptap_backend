from db.db import Connection
import time

def autofarm():
    connection = Connection()
    flag = connection.select("flags", "key", "is_my_coins_new")
    if flag[0][1] == False:
        steps = connection.select("steps", "id", "1")
        step_one = str(float(steps[0][1]))
        step = str(float(steps[0][1]) * 5)
        notcoin = str(float(steps[0][2]) * 5)
        pepe = str(float(steps[0][3]) * 5)
        shiba = str(float(steps[0][4]) * 5)
        dogecoin = str(float(steps[0][5]) * 5)
        dogwifhat = str(float(steps[0][6]) * 5)
        popcat = str(float(steps[0][7]) * 5)
        mog = str(float(steps[0][8]) * 5)
        floki = str(float(steps[0][9]) * 5)
        ponke = str(float(steps[0][10]) * 5)
        mew = str(float(steps[0][11]) * 5)
        bome = str(float(steps[0][12]) * 5)
        upd = "UPDATE coins SET auto_coins_max=auto_coins_max-" + step + ", auto_coins=auto_coins+" + step + ", notcoin_auto=notcoin_auto+" + notcoin + ", pepe_auto=pepe_auto+" + pepe + ", shiba_auto=shiba_auto+" + shiba + ", dogecoin_auto=dogecoin_auto+" + dogecoin + ", dogwifhat_auto=dogwifhat_auto+" + dogwifhat + ", popcat_auto=popcat_auto+" + popcat + ", mog_auto=mog_auto+" + mog + ", floki_auto=floki_auto+" + floki + ", ponke_auto=ponke_auto+" + ponke + ", mew_auto=mew_auto+" + mew + ", bome_auto=bome_auto+" + bome + " WHERE autoclick = true AND end_of_day_autoclick > 0 AND auto_coins_max >= " + step + ";"
        connection.updateFromStr(upd)

        connection.disconnect()

autofarm()