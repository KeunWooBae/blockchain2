import requests, json
import pandas as pd
import numpy as np
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt
import datetime, time
import openpyxl as xl
import csv

class BlockChain:

    def __init__(self):
        self.header = header
        # inputs=self.txData.get('inputs', [])
        # if inputs: #None, []
        #     if isinstance(inputs, list):
        self.errorflag = 0
        self.flag = 0

    def initAddressFromExcel(self, address):
        url = requests.get("https://blockchain.info/rawaddr/" + address, headers=self.header)
        print("initAddress 상태코드 : " + str(url.status_code))
        text = url.text
        time.sleep(5)
        self.addrData = json.loads(text)
        self.currentAddr = self.addrData['address']
        self.errorflag = url.status_code
        # with open('file_name2.json', 'w') as f:
        #     json.dump(self.addrData, f, indent=4)

    def getAddrType(self, addr):
        if addr[0] == '1':
            return "P2PKH"
        elif addr[0] == '3':
            return "P2SH"
        else:
            return "Bech32"

    def getTxHashList(self):
        txList = []
        tx_n = len(self.addrData['txs'])
        for txNum in range (0, tx_n):
            txList.append(self.addrData['txs'][txNum]['hash'])
        return txList

    def initHashInfo(self, txHashList):
        txHash1 = txHashList[0]
        txHash2 = txHashList[1]
        url = requests.get("https://blockchain.info/rawtx/" + txHash1, headers=self.header)
        print("initHash1Info 상태코드 : " + str(url.status_code))
        text = url.text
        time.sleep(5)
        self.txData1 = json.loads(text)

        # with open('file_name.json', 'w') as f:
        #     json.dump(self.txData, f, indent=4)

    def isMultiOutput(self):
        if len(self.addrData['txs'][0]['out']) == 2:
            return True
        else:
            return False

    def isSingleInput(self):
        if len(self.addrData['txs'][0]['inputs']) == 1:
            return True
        else:
            return False

    def isNewTx(self):
        if len(self.addrData['txs']) == 2:
            return True
        else:
            return False

    def noSelfAddress(self):
        firstAddress = self.addrData['txs'][0]['out'][0]['addr']
        secondAddress = self.addrData['txs'][0]['out'][1]['addr']
        if firstAddress == self.currentAddr or secondAddress == self.currentAddr:
            return False
        else:
            return True

    def getNextAddr(self):
        firstAddress = self.addrData['txs'][0]['out'][0]['addr']
        secondAddress = self.addrData['txs'][0]['out'][1]['addr']
        if self.addrData['txs'][0]['out'][0]['value'] > self.addrData['txs'][0]['out'][1]['value']:
            return firstAddress
        else:
            return secondAddress


header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp.image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

block = BlockChain()

#bring address from excel file
# location = "D:\python"
# file = "투자사기_peelchain_ver 1.0.xlsx"
# data_pd = pd.read_excel('{}/{}'.format(location, file), header=None, index_col=None, names=None)
# address = pd.DataFrame.to_numpy(data_pd)
# now = time.localtime()
# date = "%d%02d%02d%0d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
f = open('D:\python\투자사기_fee_cluster' + '.csv', 'a')
f.write("inputAddr,TxTime,Fee,Address Type,BTC received, BTC sent, BTC Balance\n")

# excel_len = len(address)
# print(excel_len)
addressList = ["1LABwuafbMBR2JCFW8bSkjDZw751TvBBnh", "1HxXzcqDvifwS216KgBReCC41isZZoD7bE", "1BNW8NoaUo1CbqLAUvZU4nozREjaoV23vS", "12L371NEwKBQUzBkur1h51t9KYBbcKky6y", "1CGwKSqa5GSvaBuobyqW2THxVcTFVefKY2", "1PYeFkUGEqKiCPFabyfbSPBEHj5x1RymdV", "1A7WfZasYHr6WSFj6dfyX4bieUaE5ieaj6",
               "19JTyZxsm6dxXu8TWXNFDg4CrajMPaNJzB", "1MX6jbuTmXAs79q2oNVhp4vLNJ3EEHEGZe", "14pLa356zaqMKCLvmtjCRHVwLRhhxQR8dG", "1E3Gudip2j1whLBxiVF5vA4knEvBhwhcJ7", "15oDEnmYDzktRFYCof7BXrQrt4iYyxqQmy", "1E4joeSALgDC5hyfhX8mXAqzSivynKwwzF", "1Bp4U7WWvzxXshiM7e12xNypfDcnN8ShD2",
               "1Js8hfCu4o3Sa7v1ss4GyVJSs3GgZXzAmq", "13AsNAfKyYGF5V5Fs7mRmXogZX1Xzzkptu", "18HqBkA8eKmkCp1uDPnJDwVvgF8x6rSsJ", "1B6joK3LVmSkiRTWHNn8rjnPrQzFkWR82h", "1EgYRFU7ACVPk5bV4FF8DhhUiK23Py9uxy", "1EW1qeku3S214fg37uCYzivxnnvttYM5rh", "18cZjN9EGYgb59h6PDCZj43cj3bko2Ba8a",
               "18rcPi5sxwWz1rsBUfv7Duzj43btNc5Ezg", "14KV7zA57eyCS9bVCe6mM54F7r3UKpNths"]
# address = "1AABsVPPRHH7CZ1SKa56xwG2BrdNZ3FMoE"
address = addressList[0]
start = 0

for x in range(1, 100000):

    f = open('D:\python\투자사기_fee_cluster' + '.csv', 'a')
    print("count : " + str(x))
    block.initAddressFromExcel(address)  #
    if block.errorflag == 200:
        if block.isSingleInput() == True and block.isMultiOutput() == True and block.noSelfAddress() == True and block.isNewTx() == True:
            print("PEEL CHAIN!")
            print("input : " + block.addrData['address'])
            uTime = block.addrData['txs'][0]['time']
            txTime = datetime.datetime.fromtimestamp(uTime)
            print("Time : " + str(txTime))
            print("Fee : " + str(block.addrData['txs'][1]['fee']))
            print("BTC received : " + str(block.addrData['total_received'] / 100000000))
            print("BTC sent : " + str(block.addrData['total_sent'] / 100000000))
            print("BTC balance : " + str(block.addrData['final_balance'] / 100000000))
            addrType = block.getAddrType(block.addrData['address'])
            f.write(block.addrData['address'] + "," + str(txTime) + "," + str(block.addrData['txs'][0]['fee']) +
                    "," + addrType + "," + str(block.addrData['total_received'] / 100000000) + "," + str(block.addrData['total_sent'] / 100000000) + "," + str(block.addrData['final_balance'] / 100000000) + "," + str(x) +"\n")
            f.close()
            address = block.getNextAddr()

        else:
            f.write("stop at" + "," + str(x) + "\n")
            f.close()
            start += 1
            address = addressList[start]

    else:
        f.write("error at" + "," + str(x) + "\n")
        f.close()
        start += 1
        address = addressList[start]
        continue


f.close()
