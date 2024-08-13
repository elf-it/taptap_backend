from db.db import Connection

types = [
    "unlimit",
    "autoclick",
    "lottery",
    "status",
    "boost",
    "withdraw"
]

status_coins = [
    7000,
    10500,
    14000,
    17500,
    21000,
    24500
]

percent_boost = [
    50,
    100,
    150,
    200,
    250
]

xcoins_unlimit = [
    0,
    5,
    6,
    7,
    8,
    10
]

tickets = [
    2, 
    12, 
    30, 
    70, 
    200
]

def setBonuses(tid: str, amount: int):
    connection = Connection()
    arr = connection.select("person", "password", tid)

    st = [5, 2, 2, 2, 2, 2]

    nref = arr[0][3]
    index = 0
    for s in st:
        if nref:
            ref = connection.select("person", "password", nref)
            if ref:
                if ref[0][4] >= index:
                    connection.update("person", ["bonuses"], [str(float(ref[0][6]) + (amount / 100 * s))], ref[0][0])
                    connection.insert("refs", ["tid", "rid", "amount"], [arr[0][2], ref[0][2], str(amount / 100 * s)])
                nref = ref[0][3]
        else:
            break
        index = index + 1
    connection.disconnect()
    return True

def updateTransactions():
    # status: 1 - created, 2 - paid, 3 - unpaid, 4 - failed
    # безлимит - 0, автофарм - 1, лотерея - 2, статус - 3, буст - 4 --- data.index
    connection = Connection()

    flag = connection.select("flags", "key", "is_my_coins_new")
    if flag[0][1] == False:

        transactions = connection.select("transactions", "status", "1")

        if transactions:
            cicle = connection.select("flags", "key", "cicle")
            for transaction in transactions:
                tid = transaction[1]
                package = types[int(transaction[6])]
                package_index = int(transaction[3]) + 1

                coins = connection.select("coins", "tid", tid)
                person = connection.select("person", "password", tid)

                if coins:
                    if package == "status":
                        if person[0][4] <= package_index:
                            connection.update("person", ["level"], [package_index], person[0][0])
                            #max = status_coins[package_index - 1] - coins[0][4] + status_coins[package_index]
                            connection.update("coins", ["status"], [status_coins[package_index]], coins[0][0])
                    elif package == "unlimit":
                        if coins[0][40] <= package_index:
                            connection.update("coins", ["unlimit", "flag_unlimit", "end_of_day_unlimit", "coins_unlimit", "tarif_unlimit"], [True, int(cicle[0][3]) + 1, 0, xcoins_unlimit[int(transaction[3])], package_index], coins[0][0])
                    elif package == "boost":
                        if coins[0][41] <= package_index:
                            connection.update("coins", ["boost", "flag_boost", "end_of_day_boost", "coins_boost", "tarif_boost"], [True, int(cicle[0][3]) + 1, 120, percent_boost[int(transaction[3])], package_index], coins[0][0])
                    elif package == "autoclick":
                        if coins[0][29] <= package_index:
                            connection.update("coins", ["autoclick", "flag_autoclick", "end_of_day_autoclick", "tarif_autoclick", "auto_coins_max"], [True, int(cicle[0][3]) + 1, package_index, package_index, 0], coins[0][0])
                    elif package == "lottery":
                        connection.update("person", ["tickets"], [tickets[int(transaction[3])]], person[0][0])
                    elif package == "withdraw":
                        connection.update("person", ["bonuses"], [0], person[0][0])

                if package != "withdraw":

                    setBonuses(transaction[1], int(transaction[4]))

                    tickets = person[0][8] + int(transaction[4])

                    connection.update("person", ["tickets"], [tickets], person[0][0])

                connection.update("transactions", ["status"], [2], transaction[0])

updateTransactions()