from db.db import Connection

newObj = []
rid = "358929635"

def getRefs(referrer):
    tid = []
    connection = Connection()
    arr = connection.select("person", "referrer", referrer)
    if arr:
        for a in arr:
            tid.append({"tid": a[2], "name": a[1], "status": a[4], "amount": 0})
    else:
        return False

    connection.disconnect()
    return tid

line1 = getRefs(rid)
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
if newObj:
    for no in range(len(newObj)):
        refs = connection.selectWhereList("refs", "tid='" + newObj[no]["tid"] + "' and rid='" + "358929635" + "'")
        if refs:
            for r in refs:
                newObj[no]["amount"] = newObj[no]["amount"] + float(r[3])

connection.disconnect()

print(newObj)