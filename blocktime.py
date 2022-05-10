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

    def initAddressFromExcel(self, address):
        url = requests.get("https://blockchain.info/rawaddr/" + address, headers=self.header)
        print("initAddress 상태코드 : " + str(url.status_code))
        text = url.text
        time.sleep(5)
        self.addrData = json.loads(text)

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

    def initAddress(self, address):
        url = requests.get("https://blockchain.info/rawaddr/" + address, headers=self.header)
        print("initAddress 상태코드 : " + str(url.status_code))
        text = url.text
        time.sleep(5)
        self.addrData = json.loads(text)

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

    def getTime(self):
        uTime = self.txData['time']
        txTime = datetime.datetime.fromtimestamp(uTime)
        return str(txTime)

    def getBalance(self):
        return self.addrData['final_balance']


header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp.image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

block = BlockChain()

#bring address from excel file
location = "D:\python"
# file = "all node.xlsx"
# data_pd = pd.read_excel('{}/{}'.format(location, file), header=None, index_col=None, names=None)
# address = pd.DataFrame.to_numpy(data_pd)
# address = '1KLsKGS1RyAUmuPG2pgCJM1B9FHeD4ezkU'
address = '14D4BuxgnB1AxPoJ25oMVQ8DC6vdq1ex7i'
address = '1KTVSLLsD4N9N3bYqfhUxbUoKZbR8GJyAa'
address = '16mMg3Cb6dTq4igsqvjuuTMt5xcAEbVVXC'
address = '1DkXjYUqVQkgBeGeiMWcKDUf78DBe58gGi'


now = time.localtime()
date = "%d%02d%02d%0d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
f = open('D:\python\peelchainTime' + date + '.csv', 'a')
f.write("Current Address,Next Address,Time,Fee\n")

nextAddr = address

for x in range(0, 1000):
    block.initAddress(nextAddr)
    txList = block.getTxHashList()

    for txhash in txList:
        block.initHashInfo(txhash)

        if block.isSingleInput() == True and block.isMultiOutput() == True:
            if block.txData['inputs'][0]['prev_out']['addr'] == block.addrData['address']:
                txTime = block.getTime()
                if block.txData['out'][0]['value'] > block.txData['out'][1]['value']:
                    nextAddr = block.txData['out'][0]['addr']
                else:
                    nextAddr = block.txData['out'][1]['addr']

                print("current addr : " + block.txData['inputs'][0]['prev_out']['addr'])
                print("next addr : " + nextAddr)
                print("Time : " + txTime)
                print("Fee : " + str(block.txData['fee']/100000000))
                print("Addr Type : " + block.getAddrType())
                print("Balacne : " + str(block.getBalance()))
                f.write(block.txData['inputs'][0]['prev_out']['addr'] + "," + nextAddr + "," + txTime + "," + str(block.txData['fee']/100000000) + "," + block.getAddrType() +
                        "," + str(block.getBalance()) + "\n")

f.close()
