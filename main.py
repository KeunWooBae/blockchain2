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
        address = "1QBbo9epqNwBctuU9EG94HXMU29329z6nh"
        self.header = header
        self.initAddressFromExcel(address)  # 파일에서 불러올 경우 나중에 지우기
        self.G = G
        txList = self.getTxHashList()
        print("txList : " + str(txList))

        for txNum in range(0, len(txList)):
            self.initHashInfo(txList[txNum])
            if self.isHeuristic1() == False: # if tx is not H1(multi-input Heuristic)
                inputList, outputList = self.notHeuristic1()
                print("input not H1 : " + str(inputList))
                print("output not H1 : " + str(outputList))
                # drawGraph
                self.drawGraph(inputList, outputList, False, txNum)

            else: # if tx is H1
                inputListH1, outputListH1 = self.isHeuristic1()
                print("input : " + str(inputListH1))
                print("output : " + str(outputListH1))
                # drawGraph
                self.drawGraph(inputListH1, outputListH1, True, txNum)

        self.showGaraph()

    def initAddressFromExcel(self, address):
        url = requests.get("https://blockchain.info/rawaddr/" + address, headers=self.header)
        print("initAddress 상태코드 : " + str(url.status_code))
        text = url.text
        self.addrData = json.loads(text)

    def getAddr(self):
        return self.addrData['address']

    def getTxHashList(self):
        txList = []
        for tx_n in range(self.addrData['n_tx']):
            txList.append(self.addrData['txs'][tx_n]['hash'])
        return txList

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

    def isHeuristic1(self):
        inputListH1 = []
        outputListH1 = []
        if self.isMultipleInput() == True:
            for num in range(0, len(self.txData['inputs'])):
                inputListH1.append(self.txData['inputs'][num]['prev_out']['addr'])

            for num in range(len(self.txData['out'])):
                outputListH1.append(self.txData['out'][num]['addr'])
            return inputListH1, outputListH1
        else:
            return False

    def notHeuristic1(self):
        inputNum = len(self.txData['inputs'])
        inputList = []
        outputNum = len(self.txData['out'])
        outputList = []

        for iN in range(0, inputNum):
            inputList.append(self.txData['inputs'][iN]['prev_out']['addr'])

        for oN in range(0, outputNum):
            outputList.append(self.txData['out'][oN]['addr'])

        return inputList, outputList

    def drawGraph(self, inputList, outputList, isH1, txNum):

        nodeName = []
        if isH1 == True:

            # node
            for iL in range(len(inputList)):
                nodeName.append(inputList[iL][0:5] + "..")
                self.G.add_node(inputList[iL][0:5] + "..")

            for oL in range(len(outputList)):
                self.G.add_node(outputList[oL][0:5] + "..")

            #edge
            for oL in range(len(outputList)):
                for iL in range(len(inputList)):
                    self.G.add_edge(nodeName[iL], outputList[oL][0:5] + "..")

            colorList = ['r', 'g', 'b']
            write_dot(self.G, 'test.dot')
            # same layout using matplotlib with no labels
            plt.title('draw_networkx')
            pos = graphviz_layout(self.G, prog='dot')
            nx.draw_networkx_nodes(self.G, pos, nodelist=nodeName, node_color=colorList[txNum])

            '''
            labels = {}
            for x in range(len(nodeName)):
                labels[x] = '$' + nodeName[x] + '$'

            #nx.draw(self.G, pos, with_labels=True, arrows=True, node_color=colorList[txNuma])
            nx.draw_networkx_nodes(self.G, pos, nodelist=nodeName, node_color=colorList[txNuma])
            nx.draw_networkx_labels(self.G, pos, labels=labels, font_size=10, font_color="whitesmoke")
            '''

        else: # if it is not H1
            #node
            self.G.add_node(inputList[0][0:5] + "..") # if it is not H1 then, single input

            for oL in range(len(outputList)):
                self.G.add_node(outputList[oL][0:5] + "..")

            #edge
            for oL in range(len(outputList)):
                self.G.add_edge(inputList[0][0:5] + "..", outputList[oL][0:5] + "..")

            colorList = ['r', 'g', 'b']
            write_dot(self.G, 'test.dot')
            # same layout using matplotlib with no labels
            plt.title('draw_networkx')
            pos = graphviz_layout(self.G, prog='dot')
            nx.draw(G, pos, with_labels=True, arrows=True, node_color='r', node_size=400)
            nx.draw_networkx_nodes(self.G, pos, nodelist=[inputList[0][0:5] + ".."], node_color='g')

    def showGaraph(self):

        plt.savefig('nx_test.png')
        plt.show()





header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp.image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

G = nx.DiGraph()
block = BlockChain()

#bring address from excel file
#location = "D:\python"
#file = "cryptocurrency.xlsx"
#data_pd = pd.read_excel('{}/{}'.format(location, file), header=None, index_col=None, names=None)
#address = pd.DataFrame.to_numpy(data_pd)
#block.initAddressFromExcel(address)