# @Copyright Joao Montenegro 2017

from web3 import Web3, KeepAliveRPCProvider, IPCProvider
import json, time, os, traceback, logging
from datetime import datetime

class EthConnection:
    '''
    Connects to an Ethereum JSON-RPC node.
    '''

    def __init__(self, host='localhost', port='8545'):
        '''
        Constructor. It does not connect here (see connect()).
        '''
        self.host = host
        self.port = port

        self.web3 = None

        self.log = logging.getLogger('EthConnection')

    def isConnected(self):
        '''
        Tells if the connection has been established.
        '''
        return self.web3 is not None

    def connect(self):
        '''
        Connects to the node. Returns True if a connection is created or already exists.

        '''
        if self.isConnected():
            print("Already connected.")
            return True

        try:
            # Connect
            self.web3 = Web3(KeepAliveRPCProvider(host=self.host, port=self.port))
        except:
            self.log.error('Error Connecting to %s:%s' % (host, port))
            traceback.print_exc()
            return False

        self.log.info('Connected to %s:%s' % (self.host, self.port))

        return True

    def getContract(self, addr, abiStr=None, abiFile=None):
        '''
        Returns a Web3 Contract object for the given address and ABI.
        The ABI can be specified as a either a json string or a json file.
        '''
        if not self.isConnected():
            self.log.warning('getContract(): Not connected')
            return None

        if abiStr and abiFile:
            self.log.warning('Only one between ABI string and ABI Json file musth be chosen.')
            return None
        if abiStr and abiFile:
            self.log.warning('Either an ABI string or ABI Json file musth be chosen.')
            return None

        abi = None
        if abiStr:
            abi = json.loads(abiStr)
        elif abiFile:
            try:
                with open(abiFile) as openedFile:
                    abi = json.load(openedFile)
            except:
                self.log.error('Loading json file: %s' % abiFile)
                return None

        if not abi:
            self.log.error('Bad ABI.')
            return None

        try:
            return self.web3.eth.contract(abi, addr)
        except:
            self.log.error('Error loading contract: %s' % addr)

        self.log.error('No contracted loaded: %s' % addr)
        return None

    def getEtherBalance(self, addr):
        '''
        Return the balance for the given address in ether.
        The address is a string with the format: "0x1234567..."
        '''
        if not self.isConnected():
            self.log.warning('getEtherBalance(): Not connected')
            return None

        return self.toEther(self.web3.eth.getBalance(addr))

    def toEther(self, value):
        return value / 1000000000000000000.0

    def toWei(self, value):
        return value * 1000000000000000000.0

    def unlock(self, addr, password):
        if not self.eosContract:
            return False

        if not self.web3.personal.unlockAccount(addr, password):
            self.log.warning("Wrong password!")
            return False
        return True

    def lock(self, addr):
        self.web3.personal.lockAccount(addr)

    def initTransaction(self, fromAddr, toAddr=None, ether=None, gas=None):
        tx = {'from':fromAddr}
        if toAddr is not None:
            tx['to'] = toAddr
        if ether is not None:
            wei = int(self.toWei(ether))
            tx['value'] = wei
        if gas is not None:
            tx['gas'] = gas
        return tx

    def sendTransaction(self, fromAddr, toAddr, ether=None, gas=None):
        tx = self.initTransaction(fromAddr, toAddr, ether, gas)
        return self.web3.eth.sendTransaction(tx)

