from db.db import Connection
import time

def autofarm():
    connection = Connection()
    steps = connection.select("steps", "id", "1")
    step = float(steps[0][1])
    notcoin = float(steps[0][2])
    pepe = float(steps[0][3])
    shiba = float(steps[0][4])
    dogecoin = float(steps[0][5])
    dogwifhat = float(steps[0][6])
    popcat = float(steps[0][7])
    mog = float(steps[0][8])
    floki = float(steps[0][9])
    ponke = float(steps[0][10])
    mew = float(steps[0][11])
    bome = float(steps[0][12])

    '''
    notcoin = (notcoin * 100 / step) * 5
    pepe = (pepe * 100 / step) * 5
    shiba = (shiba * 100 / step) * 5
    dogecoin = (dogecoin * 100 / step) * 5
    dogwifhat = (dogwifhat * 100 / step) * 5
    popcat = (popcat * 100 / step) * 5
    mog = (mog * 100 / step) * 5
    floki = (floki * 100 / step) * 5
    ponke = (ponke * 100 / step) * 5
    mew = (mew * 100 / step) * 5
    bome = (bome * 100 / step) * 5
    '''
    step = 14

    print("step now:", step)

    print("step in second:", 7000 / (60 * 60))
    
    print("notcoin:", notcoin * 100 / step)
    print("pepe:", pepe * 100 / step)
    print("shiba:", shiba * 100 / step)
    print("dogecoin:", dogecoin * 100 / step)
    print("dogwifhat:", dogwifhat * 100 / step)
    print("popcat:", popcat * 100 / step)
    print("mog:", mog * 100 / step)
    print("floki:", floki * 100 / step)
    print("ponke:", ponke * 100 / step)
    print("mew:", mew * 100 / step)
    print("bome:", bome * 100 / step)

    connection.disconnect()

autofarm()