import requests, json
import pandas as pd
import numpy as np
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt
import time, datetime

class BlockChain:

    def __init__(self):
        #
        address = "bc1qpq3ugjemv0ev3y2qde8nvpau2e7nxmjwlt0hxl"
        address2 = "1PqdbDDBk34jVpEVQyYgjgGnWh4orpSRKA"
        self.header = header
        self.G = G

        self.initAddressInfo(address2)
        txList = self.getTxHashList(address2)

        #for txHash in txList:
        self.initHashInfo(txList[0])

        self.originAddrData = self.addrData
        self.originTxData = self.txData

        if self.isOutputTx() == True:
            self.isOTCHeuristic(address2, txList[0])
            print("txList : " + str(txList))

        else:
            print("Not OTC")


        print("END")



    def isOTCHeuristic(self, addr, txHash):
        # 조건1 : 잔금주소로 추정되는 것은 이전에 쓰이지 않았던 주소여야 하며, 출금 이후 다시 사용되지 않은 주소이어야 한다. -> 시간비교, txCount == 2
        nextOutputList = self.getOutputAddr()
        possibleOTCAddr = nextOutputList[0] # OTC로 추정되는 주소
        self.initAddressInfo(possibleOTCAddr)

        # 이전에 쓰이지 않았던 주소여야 한다. 즉, nextOutputAddr의 맨 마지막 Tx가 possibleOTC의 Tx와 같아야한다.
        if self.addrData['txs'][-1]['hash'] == txHash:
            condition1 = True
        else:
            return False

        if condition1 == True and len(self.addrData['txs']) == 2: # 출금 이후 다시 사용 안되었을 경우 OTC 조건 만족
            # 첫번째 Tx가 출금 Tx이어야 한다.
            for iL in range(len(self.addrData['txs'][0]['inputs'])):
                if self.addrData['txs'][0]['inputs'][iL]['prev_out']['addr'] == self.addrData['address']:
                    condition2 = True
        else: # 출금 이후 다시 사용되었을 경우
            return False

        self.addrData = self.originAddrData
        self.txData = self.originTxData

        ## 조건2 : PossibleOTC가 들어있는 Tx output에 자기자신의 주소가 있으면 안된다.
        if condition1 == True and condition2 == True:
            for oN in range(len(self.txData['out'])):
                if self.txData['out'][oN]['addr'] == self.addrData['address']:
                    return False
            condition3 = True

        # 조건3 : Tx가 coinGeneration이면 안된다.
        if condition3 == True:
            self.testTx()
            # coinGeneration은 index 0은 addr 정상 출력, output index 1~3이 addr이 없어서 KeyError: 'addr'이 나온다.
            for txNum in range(len(self.txData['out'])):
                try:
                    if type(self.txData['out'][0]['addr']) is str:
                        continue

                except KeyError:
                    print("END")



        # 조건4: OTC 추정 지갑 제외 다른 주소들이 이미 한번씩 사용된 주소들이어야 한다.


        # 조건5: 출력주소가 2개여야 한다.(하나는 OTC, 하나는 일반)


    def isOutputTx(self):
        inputLen = len(self.txData['inputs']) # 출금주소 숫자
        for iL in range(inputLen):
            if self.txData['inputs'][iL]['prev_out']['addr'] == self.addrData['address']: # 출금 TX인지 확인
                return True

        return False

    def testTx(self):
        url = requests.get("https://blockchain.info/rawtx/4a09c7d62d9b521cec86262a01094c57b17d69a34fceafea57714663302b3e01" , headers=self.header)
        print("testTxInfo 상태코드 : " + str(url.status_code) + ", tx: test")
        text = url.text
        self.txData = json.loads(text)

    def isCoinBase(self):
        self.txData['out'][1]
        return True

    def initAddressInfo(self, address):
        url = requests.get("https://blockchain.info/rawaddr/" + address, headers=self.header)
        print("initAddress 상태코드 : " + str(url.status_code) + ", addr : " + address)
        text = url.text
        self.addrData = json.loads(text)

    def initHashInfo(self, txHash):
        url = requests.get("https://blockchain.info/rawtx/" + txHash, headers=self.header)
        print("initHashInfo 상태코드 : " + str(url.status_code) + ", tx: " + txHash)
        text = url.text
        self.txData = json.loads(text)



    def getAddr(self):
        return self.addrData['address']

    def getOutputAddr(self):
        outputNum = len(self.txData['out'])
        outputList = []

        for oN in range(outputNum):
            outputList.append(self.txData['out'][oN]['addr'])

        return outputList

    def getTxHashList(self, addr):
        txList = []
        for tx_n in range(self.addrData['n_tx']):
            txList.append(self.addrData['txs'][tx_n]['hash'])
        return txList


    def getTxTime(self):
        unixTime = self.txData['time']
        timeDate = datetime.datetime.fromtimestamp(unixTime).strftime('%Y-%m-%d %H:%M:%S')

        return timeDate







header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp.image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

G = nx.DiGraph()
block = BlockChain()

