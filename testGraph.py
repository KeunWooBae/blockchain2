import requests, json
import pandas as pd
import numpy as np
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt
import time

class BlockChain:

    def __init__(self):
        #
        address = "3HUeVTsa3pw1dNcqY4Tv3Lr9RMdA1WQfxa"
        self.header = header
        self.initHashInfo(address)
        self.isOutput()

    def initHashInfo(self, txHash):
        url = requests.get("https://blockchain.info/rawtx/" + txHash, headers=self.header)
        print("initHashInfo 상태코드 : " + str(url.status_code))
        text = url.text
        self.txData = json.loads(text)

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

    def isOutput(self):
        inputNum = list()
        outputNum = list()
        for txNum in (0, 100):
            for tNum in len(self.txData['tx'][txNum]['inputs']):
                inputNum.append(len(self.txData['tx'][tNum]['inputs']))
                outputNum.append(len(self.txData['tx'][tNum]['out']))

        for x in inputNum:
            for y in outputNum:
                if self.txData['tx'][]['inputs'][x]['prev_out']['addr'] == self.txData['address']:
                    if self.txData['out'][outputNum]['addr'] == self.txData['address']:
                        break
                else:
                    print("output : " + self.txData['out'][0]['addr'])

        return True


header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp.image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

block = BlockChain()
