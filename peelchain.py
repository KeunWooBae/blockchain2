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

    def initAddressFromExcel(self, address):
        url = requests.get("https://blockchain.info/rawaddr/" + address, headers=self.header)
        print("initAddress 상태코드 : " + str(url.status_code))
        text = url.text
        time.sleep(5)
        self.addrData = json.loads(text)
        self.errorflag = url.status_code
        # with open('file_name2.json', 'w') as f:
        #     json.dump(self.addrData, f, indent=4)

    def getAddrType(self):
        if self.addrData['address'][0] == '1':
            return "P2PKH"
        elif self.addrData['address'][0] == '3':
            return "P2SH"
        else:
            return "Bech32"

        return self.addrData['address']

    def getTxHashList(self):
        txList = []
        tx_n = len(self.addrData['txs'])
        for txNum in range (0, tx_n):
            txList.append(self.addrData['txs'][txNum]['hash'])
        return txList

    def initHashInfo(self, txHash):
        url = requests.get("https://blockchain.info/rawtx/" + txHash, headers=self.header)
        print("initHashInfo 상태코드 : " + str(url.status_code))
        text = url.text
        time.sleep(5)
        self.txData = json.loads(text)
        # with open('file_name.json', 'w') as f:
        #     json.dump(self.txData, f, indent=4)

    def isMultipleInput(self):
        if len(self.txData['inputs']) >= 2:
            return True #
        else: # Single Input
            return False

    def isSingleOutput(self):
        if len(self.txData['out']) == 1:
            return True #
        else:
            return False

    def isMultiOutput(self):
        if len(self.txData['out']) == 2:
            return True
        return False

    def isSingleInput(self):
        if len(self.txData['inputs']) == 1:
            return True
        return False

    def isPeelingChainCurr(self):
        if self.isSingleInput() == True and self.isMultiOutput() == True:  # 1 input & 2 output
            if self.txData['inputs'][0]['prev_out']['addr'] == self.addrData['address']:  # input address is current address
                if self.txData['out'][0]['addr'] != self.addrData['address'] and self.txData['out'][1]['addr'] != self.addrData['address']:  # output is not change address
                    return True
        return False

    def isPeelingChainPrev(self):
        if self.isSingleInput() == True and self.isMultiOutput() == True:  # 1 input & 2 output
            if self.txData['out'][0]['addr'] == self.addrData['address'] or self.txData['out'][1]['addr'] == self.addrData['address']:  # one of output address is current address
                inputAddr = self.txData['inputs'][0]['prev_out']['addr']
                outAddr1 = self.txData['out'][0]['addr']
                outAddr2 = self.txData['out'][1]['addr']
                if inputAddr != outAddr1 and inputAddr != outAddr2:
                    return True
        return False

    def getPeelingRatio(self):
        if self.txData['out'][0]['value'] > self.txData['out'][1]['value']:
            return str((block.txData['out'][0]['value'] / 100000000) / (block.txData['out'][1]['value'] / 100000000))
        else:
            return str((block.txData['out'][1]['value'] / 100000000) / (block.txData['out'][0]['value'] / 100000000))



header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp.image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

block = BlockChain()

#bring address from excel file
location = "D:\python"
file = "투자사기_지갑주소.xlsx"
data_pd = pd.read_excel('{}/{}'.format(location, file), header=None, index_col=None, names=None)
address = pd.DataFrame.to_numpy(data_pd)
now = time.localtime()
date = "%d%02d%02d%0d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
f = open('D:\python\투자사기_peelchain' + date + '.csv', 'a')
f.write("inputAddr,outputAddr1,outputAddr2,inputBTC,outputBTC1,outputBTC2,peeling ratio,TxTime,Fee,Address Type\n")

excel_len = len(address)
print(excel_len)
for x in range(5249, excel_len):
    print("count : " + str(x))
    block.initAddressFromExcel(address[x][0])
    if block.errorflag == 200:
        # address = "12iScVDd2Z5c2qo3aSHBtjFmBRcsBJXQVV"
        txList = block.getTxHashList()
        txNum = len(txList)
        if txNum == 2:
            txhash1, txhash2 =  txList[0], txList[1]
            block.initHashInfo(txhash1)
            if txNum == 2:
                if block.isPeelingChainCurr() == True:
                    block.initHashInfo(txhash2)
                    if block.isPeelingChainPrev() == True:
                        block.initHashInfo(txhash1)
                        print("PEEL CHAIN!")
                        print("input : " + block.addrData['address'])
                        print("output : " + block.txData['out'][0]['addr'] + ', ' + block.txData['out'][1]['addr'])
                        print("input BTC : " + str(block.txData['inputs'][0]['prev_out']['value'] / 100000000))
                        print("output BTC : " + str(block.txData['out'][0]['value'] / 100000000) + ", " + str(
                            block.txData['out'][1]['value'] / 100000000))
                        ratio = block.getPeelingRatio()
                        print("ratio : " + ratio + " : 1")
                        uTime = block.txData['time']
                        txTime = datetime.datetime.fromtimestamp(uTime)
                        print("Time : " + str(txTime))
                        print("Fee : " + str(block.txData['fee']))
                        addrType = block.getAddrType()
                        print("Current address(input) Type : " + addrType)

                        f.write(
                            block.addrData['address'] + "," + block.txData['out'][0]['addr'] + "," + block.txData['out'][1][
                                'addr'] + "," +
                            str(block.txData['inputs'][0]['prev_out']['value'] / 100000000) + "," + str(
                                block.txData['out'][0]['value'] / 100000000) + "," +
                            str(block.txData['out'][1]['value'] / 100000000) + "," + ratio + " : " + "1" + "," +
                            str(txTime) + "," + str(block.txData['fee']) + "," + addrType + "\n")

    else:
        continue





f.close()
