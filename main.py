import requests
import json
import time

def updateData(url, filename):
    r = requests.get(url)
    json.dump(r.json(), open(filename, 'w'), indent=4)
    fileData = json.load(open(filename))
    return fileData

def getPairs(data):
    """
    gets pairs.from and pairs.to combining them, and returns a list of pairs
    """
    pairs = []
    for i in range(len(data['pairs'])):
        pairString = str(data['pairs'][i]['from'] + data['pairs'][i]['to'])
        pairs.append(pairString)
    return pairs

def getOpenInterests(data):
    """
    gets openInterests and returns a list of openInterests
    """
    openInterests = []
    for i in range(len(data['openInterests'])):
        openInterests.append(data['openInterests'][i])
    return openInterests

def linkPairsAndOpenInterests(pairs, openInterests):
    """
    linking data pairs and openInterests, returns a dictionary with key: pair and value: openInterest
    example: {'BTCUSD': {'long':'10', 'short':'11', 'max':'12'}, 'ETHUSD': {'long':'10', 'short':'11', 'max':'12'}, ...}}
    """
    d = {}
    for i in range(len(pairs)):
        d[pairs[i]] = openInterests[i]
    return d

def divideData(data):
    """
    divides (long, short, max) by 10**18, returns a dictionary with key: pair and value: {long, short, max} divided by 10**18
    """
    for i in data:
        for j in data[i]:
            data[i][j] = int(data[i][j])/(10**18)
    return data

def filterSpecificPairs(data, *args):
    s = {}
    for i in range(len(args)):
        s[args[i]] = data[args[i]]
    return s

def messageOnchange(data):
    """
    sends message when data changes using difference of a set
    """
    ...

def catchChange(data, func):
    """
    catches change of data
    """
    if data == {}:
        return set()
    else:
        s = {}
        for i in data:
            print("_DATA_")
            print({data[i]['short']}-{func})
         
        return s

def updateLinkDivideFilter(url, filename, *args):
    data = updateData(url, filename)
    linkedData = linkPairsAndOpenInterests(getPairs(data), getOpenInterests(data))
    dividedData = divideData(linkedData)
    specificPairs = filterSpecificPairs(dividedData, *args)
    return specificPairs
    
if __name__ == '__main__':
    URL = 'https://backend-arbitrum.gains.trade/trading-variables'
    FILENAME = 'data.json'
    specificPairs = {}

    specificPairs = updateLinkDivideFilter(URL, FILENAME, "ETHUSD", "NVDAUSD", "BTCUSD")
    while True:
        previousData = specificPairs
        specificPairs = updateLinkDivideFilter(URL, FILENAME, "ETHUSD", "NVDAUSD", "BTCUSD")
        if previousData and specificPairs != {}:
            for i in specificPairs:
                if previousData[i]['short'] != specificPairs[i]['short']:
                    print(f"{specificPairs[i]} short changed from:", previousData[i]['short'], "to", specificPairs[i]['short'])
                else:
                    print(f"{specificPairs} short not changed")

        time.sleep(60)
