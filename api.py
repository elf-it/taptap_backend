from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.db import Connection
import os
import json
import csv
from dotenv import load_dotenv
from pytoniq_core.boc import Cell
from decimal import *

load_dotenv()

app = FastAPI()

origins = [
    "*",
    "http://localhost:5173",
    "https://hammerhead-app-lqwus.ondigitalocean.app",
    "https://mamotic-app-mvo75.ondigitalocean.app",
    "https://app.mamotik.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def getLangIn():
    data = {}
        
    csvFilePath = r'lang.csv'

    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            key = rows['page_name']
            key2 = rows['text_name']
            if key not in data:
                data[key] = {}
            data[key][key2] = rows
    return data

statusFromFriends = [
    (3, 1, 10500),
    (6, 2, 14000),
    (12, 3, 17500),
    (24, 4, 21000),
    (100, 5, 24500)
]

@app.post("/registration")
async def registration(obj: Union[dict, None] = None):
    print(obj)
    if obj["key"] != os.getenv("SERVICE_AUTH_TOKEN"):
        return {"error": "Invalid key"}
    
    if "username" not in obj:
        obj["username"] = "user" + str(obj["tid"])

    referrer = None
    if "referrer" in obj:
        referrer = obj["referrer"]

    connection = Connection()
    refer = connection.select("person", "password", referrer)
    if not refer:
        return {"error": "noref"}

    arr = connection.select("person", "password", obj["tid"])

    lang = "en_lang"

    if "lang" in obj:
        lang = obj["lang"] + "_lang"

        csvFilePath = r'lang.csv'

        with open(csvFilePath, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)
            for rows in csvReader:
                if lang not in rows:
                    lang = "en_lang"
                break

    if not arr:
        if referrer == None:
            connection.insert("person", ["username", "password", "lang"], [obj["username"], obj["tid"], lang])
        else:
            connection.insert("person", ["username", "password", "referrer", "lang"], [obj["username"], obj["tid"], referrer, lang])
        
            refs = connection.select("person", "password", referrer)
        
            refls = connection.select("person", "referrer", referrer)
            if refs:
                num = 0
                st = 7000
                count = len(refls)
                for sff in statusFromFriends:
                    if count >= sff[0]:
                        num = sff[1]
                        st = sff[2]
                        break
                connection.update("person", ["level"], [num], refs[0][0])
                cns = connection.select("coins", "tid", refs[0][2])
                connection.update("coins", ["status"], [st], cns[0][0])

        my_coins = 0
        auto_coins = 0
        my_coins_max = 7000
        my_coins_max_static = 7000
        auto_coins_max = 7000
        status = 7000
        #tokens
        Notcoin = 0
        Pepe = 0
        Shiba = 0
        Dogecoin = 0
        Dogwifhat = 0
        Popcat = 0
        Mog = 0
        Floki = 0
        Ponke = 0
        Mew = 0
        Bome = 0

        Notcoin_auto = 0
        Pepe_auto = 0
        Shiba_auto = 0
        Dogecoin_auto = 0
        Dogwifhat_auto = 0
        Popcat_auto = 0
        Mog_auto = 0
        Floki_auto = 0
        Ponke_auto = 0
        Mew_auto = 0
        Bome_auto = 0

        connection.insert("coins", ["tid", "my_coins", "auto_coins", "my_coins_max", "auto_coins_max", "Notcoin", "Pepe", "Shiba", "Dogecoin", "Dogwifhat", "Popcat", "Mog", "Floki", "Ponke", "Mew", "Bome", "Notcoin_auto", "Pepe_auto", "Shiba_auto", "Dogecoin_auto", "Dogwifhat_auto", "Popcat_auto", "Mog_auto", "Floki_auto", "Ponke_auto", "Mew_auto", "Bome_auto", "my_coins_max_static", "status"], [obj["tid"], my_coins, auto_coins, my_coins_max, auto_coins_max, Notcoin, Pepe, Shiba, Dogecoin, Dogwifhat, Popcat, Mog, Floki, Ponke, Mew, Bome, Notcoin_auto, Pepe_auto, Shiba_auto, Dogecoin_auto, Dogwifhat_auto, Popcat_auto, Mog_auto, Floki_auto, Ponke_auto, Mew_auto, Bome_auto, my_coins_max_static, status])
    else:
        connection.disconnect()
        return arr
    
    arr2 = connection.select("person", "password", obj["tid"])
    connection.disconnect()
    return arr2

@app.post("/setaddress")
async def setAddress(obj: Union[dict, None] = None):
    if obj["key"] != os.getenv("SERVICE_AUTH_TOKEN"):
        return {"error": "Invalid key"}
    
    if "tid" not in obj:
        return {"error": "Invalid tid"}
    
    if "address" not in obj:
        return {"error": "Invalid address"}
    
    connection = Connection()
    
    person = connection.select("person", "password", obj["tid"])

    connection.update("person")

@app.post("/getsteps")
async def getSteps(obj: Union[dict, None] = None):
    if obj["key"] != os.getenv("SERVICE_AUTH_TOKEN"):
        return {"error": "Invalid key"}
    
    connection = Connection()
    arr = connection.select("steps")
    return {"step": arr[0][1], "notcoin_step": arr[0][2], "pepe_step": arr[0][3], "shiba_step": arr[0][4], "dogecoin_step": arr[0][5], "dogwifhat_step": arr[0][6], "popcat_step": arr[0][7], "mog_step": arr[0][8], "floki_step": arr[0][9], "ponke_step": arr[0][10], "mew_step": arr[0][11], "bome_step": arr[0][12]}

@app.post("/getperson")
async def getPerson(obj: Union[dict, None] = None):
    if obj["key"] != os.getenv("SERVICE_AUTH_TOKEN"):
        return {"error": "Invalid key"}
    
    if "tid" not in obj:
        return {"error": "Invalid tid"}

    connection = Connection()
    arr = connection.select("person", "password", obj["tid"])

    if not arr:
        connection.disconnect()
        return {"error": "user not found"}

    coins = connection.select("coins", "tid", obj["tid"])
    my_coins = 0
    auto_coins = 0
    my_coins_max = 7000
    my_coins_max_static = 7000
    auto_coins_max = 7000
    coins_unlimit = 1
    coins_boost = 0
    #tokens
    Notcoin = 0
    Pepe = 0
    Shiba = 0
    Dogecoin = 0
    Dogwifhat = 0
    Popcat = 0
    Mog = 0
    Floki = 0
    Ponke = 0
    Mew = 0
    Bome = 0

    Notcoin_auto = 0
    Pepe_auto = 0
    Shiba_auto = 0
    Dogecoin_auto = 0
    Dogwifhat_auto = 0
    Popcat_auto = 0
    Mog_auto = 0
    Floki_auto = 0
    Ponke_auto = 0
    Mew_auto = 0
    Bome_auto = 0

    if coins:
        my_coins = coins[0][2]
        auto_coins = coins[0][3]
        my_coins_max = coins[0][4]
        auto_coins_max = coins[0][5]
        Notcoin = coins[0][6]
        Pepe = coins[0][7]
        Shiba = coins[0][8]
        Dogecoin = coins[0][9]
        Dogwifhat = coins[0][10]
        Popcat = coins[0][11]
        Mog = coins[0][12]
        Floki = coins[0][13]
        Ponke = coins[0][14]
        Mew = coins[0][15]
        Bome = coins[0][16]
        Notcoin_auto = coins[0][17]
        Pepe_auto = coins[0][18]
        Shiba_auto = coins[0][19]
        Dogecoin_auto = coins[0][20]
        Dogwifhat_auto = coins[0][21]
        Popcat_auto = coins[0][22]
        Mog_auto = coins[0][23]
        Floki_auto = coins[0][24]
        Ponke_auto = coins[0][25]
        Mew_auto = coins[0][26]
        Bome_auto = coins[0][27]

        Notcoin = Notcoin + Notcoin_auto
        Pepe = Pepe + Pepe_auto
        Shiba = Shiba + Shiba_auto
        Dogecoin = Dogecoin + Dogecoin_auto
        Dogwifhat = Dogwifhat + Dogwifhat_auto
        Popcat = Popcat + Popcat_auto
        Mog = Mog + Mog_auto
        Floki = Floki + Floki_auto
        Ponke = Ponke + Ponke_auto
        Mew = Mew + Mew_auto
        Bome = Bome + Bome_auto

        my_coins_max_static = coins[0][32]

        coins_unlimit = coins[0][42]
        coins_boost = coins[0][44]

    fl = connection.select("flags", "key", "cicle")
    timer = fl[0][4]

    ticketsStatus = {
        "begin": 0,
        "silver": 0,
        "gold": 0,
        "platinum": 0,
        "black": 0,
        "ultima": 0
    }

    allUsers = connection.select("person")
    for au in allUsers:
        if au[4] == 0:
            ticketsStatus["begin"] = ticketsStatus["begin"] + au[8]
        elif au[4] == 1:
            ticketsStatus["silver"] = ticketsStatus["silver"] + au[8]
        elif au[4] == 2:
            ticketsStatus["gold"] = ticketsStatus["gold"] + au[8]
        elif au[4] == 3:
            ticketsStatus["platinum"] = ticketsStatus["platinum"] + au[8]
        elif au[4] == 4:
            ticketsStatus["black"] = ticketsStatus["black"] + au[8]
        elif au[4] == 5:
            ticketsStatus["ultima"] = ticketsStatus["ultima"] + au[8]

    connection.disconnect()

    autoclick = False
    if coins[0][33] == True and coins[0][30] > 0 and coins[0][5] > 0:
        autoclick = True

    lng = getLangIn()
    stats = [
        lng["stats"]["get_begin"][arr[0][7]],
        lng["stats"]["get_silver"][arr[0][7]],
        lng["stats"]["get_gold"][arr[0][7]],
        lng["stats"]["get_platinum"][arr[0][7]],
        lng["stats"]["get_black"][arr[0][7]],
        lng["stats"]["get_ultima"][arr[0][7]]
    ]

    return {"tid": arr[0][2], "username": arr[0][1], "level": arr[0][4], "status": stats[arr[0][4]], "bonuses": round(float(arr[0][6]), 2), "my_coins": my_coins, "auto_coins": auto_coins, "my_coins_max": my_coins_max, "auto_coins_max": auto_coins_max, "Notcoin": Notcoin, "Pepe": Pepe, "Shiba": Shiba, "Dogecoin": Dogecoin, "Dogwifhat": Dogwifhat, "Popcat": Popcat, "Mog": Mog, "Floki": Floki, "Ponke": Ponke, "Mew": Mew, "Bome": Bome, "Notcoin_auto": Notcoin_auto, "Pepe_auto": Pepe_auto, "Shiba_auto": Shiba_auto, "Dogecoin_auto": Dogecoin_auto, "Dogwifhat_auto": Dogwifhat_auto, "Popcat_auto": Popcat_auto, "Mog_auto": Mog_auto, "Floki_auto": Floki_auto, "Ponke_auto": Ponke_auto, "Mew_auto": Mew_auto, "Bome_auto": Bome_auto, "my_coins_max_static": my_coins_max_static, "autoclick": autoclick, "status_autoclick": coins[0][33], "status_unlimit": coins[0][35], "status_boost": coins[0][38], "timer": timer, "lang": arr[0][7], "tickets": arr[0][8], "ticketsStatus": ticketsStatus, "coins_unlimit": coins_unlimit, "coins_boost": coins_boost}

def getRefs(referrer):
    
    tid = []
    connection = Connection()
    arr = connection.select("person", "referrer", referrer)
    if arr:
        for a in arr:
            
            tid.append({"tid": str(a[2]), "name": a[1], "status": a[4], "coins": 0})
    else:
        return False

    connection.disconnect()
    return tid

@app.post("/getreferals")
async def getReferals(obj: Union[dict, None] = None):
    if obj["key"] != os.getenv("SERVICE_AUTH_TOKEN"):
        return {"error": "Invalid key"}

    if "tid" not in obj:
        return {"error": "Invalid tid r"}
    
    newObj = []

    line1 = getRefs(obj["tid"])
    if line1:
        newObj = [*newObj, *line1]
        for l1 in line1:
            line2 = getRefs(l1["tid"])
            if line2:
                newObj = [*newObj, *line2]
                for l2 in line2:
                    line3 = getRefs(l2["tid"])
                    if line3:
                        newObj = [*newObj, *line3]
                        for l3 in line3:
                            line4 = getRefs(l3["tid"])
                            if line4:
                                newObj = [*newObj, *line4]
                                for l4 in line4:
                                    line5 = getRefs(l4["tid"])
                                    if line5:
                                        newObj = [*newObj, *line5]

    connection = Connection()

    lng = getLangIn()

    arrLang = connection.select("person", "password", obj["tid"])

    stats = [
        lng["stats"]["get_begin"][arrLang[0][7]],
        lng["stats"]["get_silver"][arrLang[0][7]],
        lng["stats"]["get_gold"][arrLang[0][7]],
        lng["stats"]["get_platinum"][arrLang[0][7]],
        lng["stats"]["get_black"][arrLang[0][7]],
        lng["stats"]["get_ultima"][arrLang[0][7]]
    ]

    if newObj:
        for no in range(len(newObj)):
            refs = connection.selectWhereList("refs", "tid='" + newObj[no]["tid"] + "' and rid='" + str(obj["tid"]) + "'")
            if refs:
                for r in refs:
                    newObj[no]["coins"] = newObj[no]["coins"] + float(r[3])
            newObj[no]["status"] = stats[newObj[no]["status"]]
            newObj[no]["coins"] = round(newObj[no]["coins"], 2)

    connection.disconnect()

    return {"referals": newObj}

@app.post("/getautoclick")
async def getAutoclick(obj: Union[dict, None] = None):
    if obj["key"] != os.getenv("SERVICE_AUTH_TOKEN"):
        return {"error": "Invalid key"}

    connection = Connection()
    arr = connection.select("autoclick", "uid", obj["tid"])
    connection.disconnect()
    if not arr:
        return {"tid": obj["tid"], "index": 0, "day": 0, "second": 0, "status": False}
    
    return {"tid": arr[0][1], "index": arr[0][2], "day": arr[0][3], "second": arr[0][4], "status": arr[0][5]}

@app.post("/setmycoins")
async def setMyCoins(obj: Union[dict, None] = None):
    print(obj)
    if obj["key"] != os.getenv("SERVICE_AUTH_TOKEN"):
        return {"error": "Invalid key"}
    
    if "amount" not in obj:
        return {"error": "no amount"}
    
    if "max_amount" not in obj:
        return {"error": "no max_amount"}
    
    if "tid" not in obj:
        return {"error": "no tid"}
    
    if "coins" not in obj:
        return {"error": "not coins"}
    
    connection = Connection()

    arr = connection.select("coins", "tid", obj["tid"])

    if arr:
        flag = connection.select("flags", "key", "is_my_coins_new")
        if flag[0][1] == False:
            max_amount = arr[0][4]
            if obj["max_amount"] < arr[0][4]:
                max_amount = obj["max_amount"]

            getcontext().prec = 6

            Notcoin = arr[0][6] + Decimal(obj["coins"]["Notcoin"])
            Pepe = arr[0][7] + Decimal(obj["coins"]["Pepe"])
            Shiba = arr[0][8] + Decimal(obj["coins"]["Shiba"])
            Dogecoin = arr[0][9] + Decimal(obj["coins"]["Dogecoin"])
            Dogwifhat = arr[0][10] + Decimal(obj["coins"]["Dogwifhat"])
            Popcat = arr[0][11] + Decimal(obj["coins"]["Popcat"])
            Mog = arr[0][12] + Decimal(obj["coins"]["Mog"])
            Floki = arr[0][13] + Decimal(obj["coins"]["Floki"])
            Ponke = arr[0][14] + Decimal(obj["coins"]["Ponke"])
            Mew = arr[0][15] + Decimal(obj["coins"]["Mew"])
            Bome = arr[0][16] + Decimal(obj["coins"]["Bome"])

            connection.update("coins", ["my_coins", "my_coins_max", "Notcoin", "Pepe", "Shiba", "Dogecoin", "Dogwifhat", "Popcat", "Mog", "Floki", "Ponke", "Mew", "Bome"], [arr[0][2] + Decimal(obj["amount"]), max_amount, Notcoin, Pepe, Shiba, Dogecoin, Dogwifhat, Popcat, Mog, Floki, Ponke, Mew, Bome], arr[0][0])

        am = connection.select("coins", "tid", obj["tid"])

        connection.disconnect()

        return {"my_coins": am[0][2], "auto_coins": am[0][3], "my_coins_max": am[0][4], "auto_coins_max": am[0][5], "Notcoin": am[0][6], "Pepe": am[0][7], "Shiba": am[0][8], "Dogecoin": am[0][9], "Dogwifhat": am[0][10], "Popcat": am[0][11], "Mog": am[0][12], "Floki": am[0][13], "Ponke": am[0][14], "Mew": am[0][15], "Bome": am[0][16]}
    else:
        connection.disconnect()
        return {"my_coins": 0, "auto_coins": 0, "my_coins_max": 0, "auto_coins_max": 0, "Notcoin": 0, "Pepe": 0, "Shiba": 0, "Dogecoin": 0, "Dogwifhat": 0, "Popcat": 0, "Mog": 0, "Floki": 0, "Ponke": 0, "Mew": 0, "Bome": 0}

@app.post("/createtx")
async def createTX(obj: Union[dict, None] = None):
    if obj["key"] != os.getenv("SERVICE_AUTH_TOKEN"):
        return {"error": "Invalid key"}
    
    if "txhash" not in obj:
        return {"error": "no txhash"}
    if "package" not in obj:
        return {"error": "no package"}
    if "package_index" not in obj:
        return {"error": "no package index"}
    if "amount" not in obj:
        return {"error": "no amount"}
    if "tid" not in obj:
        return {"error": "no tid"}
    
    connection = Connection()
    otx = connection.select("transactions", "txhash", obj["txhash"])

    if otx:
        return {"error": "txhash already exists"}
    
    # status: 1 - created, 2 - paid, 3 - unpaid, 4 - failed
    # безлимит - 0, автофарм - 1, лотерея - 2, статус - 3, буст - 4 --- data.index
    #msg_hash = Cell.one_from_boc(obj["txhash"]).hash.hex()
    connection.insert("transactions", ["uid", "txhash", "package_index", "amount", "status", "package"], [obj["tid"], obj["txhash"], obj["package_index"], obj["amount"], 1, obj["package"]])
            
    connection.disconnect()

    return {"hash": obj["txhash"]}

@app.post("/setlang")
async def setLang(obj: Union[dict, None] = None):
    if obj["key"] != os.getenv("SERVICE_AUTH_TOKEN"):
        return {"error": "Invalid key"}
    
    if "tid" not in obj:
        return {"error": "no tid"}

    if "lang" not in obj:
        return {"error": "no lang"}
    
    lang = obj["lang"]
        
    csvFilePath = r'lang.csv'

    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            if lang not in rows:
                lang = "en_lang"
            break
    
    connection = Connection()

    person = connection.select("person", "password", obj["tid"])

    connection.update("person", ["lang"], [lang], person[0][0])

    connection.disconnect()

    return True

@app.post("/getlang")
async def getLang():
    data = {}
        
    csvFilePath = r'lang.csv'

    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            key = rows['page_name']
            key2 = rows['text_name']
            if key not in data:
                data[key] = {}
            data[key][key2] = rows
    return data