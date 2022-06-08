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
f = open('D:\python\투자사기_fee3' + '.csv', 'a')
f.write("inputAddr,TxTime,Fee,Address Type\n")

# excel_len = len(address)
# print(excel_len)
address = "1AABsVPPRHH7CZ1SKa56xwG2BrdNZ3FMoE"

for x in range(882, 1500):

    f = open('D:\python\투자사기_fee3' + '.csv', 'a')
    print("count : " + str(x))
    block.initAddressFromExcel(address)  #
    if block.errorflag == 200:
        if block.isSingleInput() == True and block.isMultiOutput() == True:
            if block.noSelfAddress() == True:
                if block.isNewTx() == True:
                    # 출금 트랜잭션 정보 = txData1
                    print("PEEL CHAIN!")
                    # print("input : " + block.addrData['address'])
                    # print("output : " + block.txData1['out'][0]['addr'] + ', ' + block.txData1['out'][1]['addr'])
                    # print("input BTC : " + str(block.txData1['inputs'][0]['prev_out']['value'] / 100000000))
                    # print("output BTC : " + str(block.txData1['out'][0]['value'] / 100000000) + ", " + str(
                    #     block.txData1['out'][1]['value'] / 100000000))
                    # ratio = block.getPeelingRatio()
                    # print("ratio : " + ratio + " : 1")
                    print("input : " + block.addrData['address'])
                    uTime = block.addrData['txs'][0]['time']
                    txTime = datetime.datetime.fromtimestamp(uTime)
                    print("Time : " + str(txTime))
                    print("Fee : " + str(block.addrData['txs'][1]['fee']))
                    addrType = block.getAddrType(block.addrData['address'])
                    f.write(block.addrData['address'] + "," + str(txTime) + "," + str(block.addrData['txs'][0]['fee']) +
                            "," + addrType + "," + str(x) + "," + "\n")
                    # print("Fee : " + str(block.txData1['fee']))
                    # addrType = block.getAddrType(block.addrData['address'])
                    # print("Current address(input) Type : " + addrType)
                    #
                    # f.write(
                    #     block.addrData['address'] + "," + block.txData1['out'][0]['addr'] + "," +
                    #     block.txData1['out'][1][
                    #         'addr'] + "," +
                    #     str(block.txData1['inputs'][0]['prev_out']['value'] / 100000000) + "," + str(
                    #         block.txData1['out'][0]['value'] / 100000000) + "," +
                    #     str(block.txData1['out'][1]['value'] / 100000000) + "," + ratio + " : " + "1" + "," +
                    #     str(txTime) + "," + str(block.txData1['fee']) + "," + addrType + "\n")

                    f.close()
                    address = block.getNextAddr()



    else:
        f.write("error at" + "," + str(x) + "\n")
        f.close()
        continue





f.close()
