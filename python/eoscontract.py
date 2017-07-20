# @Copyright Joao Montenegro 2017

from ethconnection import EthConnection

EOS_ICO_CONTRACT_ADDR = '0xd0a6E6C54DbC68Db5db3A091B171A77407Ff7ccf'
EOS_ICO_CONTRACT_ABI = '[{"constant":true,"inputs":[{"name":"","type":"uint256"},{"name":"","type":"address"}],"name":"claimed","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"owner_","type":"address"}],"name":"setOwner","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"time","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint128"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"foundersAllocation","outputs":[{"name":"","type":"uint128"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"day","type":"uint256"}],"name":"claim","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"foundersKey","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"},{"name":"","type":"address"}],"name":"userBuys","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"day","type":"uint256"}],"name":"createOnDay","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"freeze","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"keys","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"startTime","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"authority_","type":"address"}],"name":"setAuthority","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"dailyTotals","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"buy","outputs":[],"payable":true,"type":"function"},{"constant":true,"inputs":[],"name":"openTime","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"EOS","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"today","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"authority","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"eos","type":"address"}],"name":"initialize","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"createFirstDay","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"claimAll","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"timestamp","type":"uint256"}],"name":"dayFor","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"day","type":"uint256"},{"name":"limit","type":"uint256"}],"name":"buyWithLimit","outputs":[],"payable":true,"type":"function"},{"constant":false,"inputs":[],"name":"collect","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"numberOfDays","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"key","type":"string"}],"name":"register","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"createPerDay","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"inputs":[{"name":"_numberOfDays","type":"uint256"},{"name":"_totalSupply","type":"uint128"},{"name":"_openTime","type":"uint256"},{"name":"_startTime","type":"uint256"},{"name":"_foundersAllocation","type":"uint128"},{"name":"_foundersKey","type":"string"}],"payable":false,"type":"constructor"},{"payable":true,"type":"fallback"},{"anonymous":false,"inputs":[{"indexed":false,"name":"window","type":"uint256"},{"indexed":false,"name":"user","type":"address"},{"indexed":false,"name":"amount","type":"uint256"}],"name":"LogBuy","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"window","type":"uint256"},{"indexed":false,"name":"user","type":"address"},{"indexed":false,"name":"amount","type":"uint256"}],"name":"LogClaim","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"user","type":"address"},{"indexed":false,"name":"key","type":"string"}],"name":"LogRegister","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"LogCollect","type":"event"},{"anonymous":false,"inputs":[],"name":"LogFreeze","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"authority","type":"address"}],"name":"LogSetAuthority","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"}],"name":"LogSetOwner","type":"event"}]'


class EOSContract (EthConnection):
    '''
    Creates a connection to the EOS ICO contract.
    '''

    def __init__(self, myAddr, host='localhost', port='8545'):
        '''
        Constructor.
        Takes your account address.
        '''
        EthConnection.__init__(self, host, port)

        self.eosContract = None
        self.myAddr = myAddr

    def connect(self):
        '''
        Connect
        '''
        if not EthConnection.connect(self):
            return False

        self.eosContract = self.getContract(
            addr=EOS_ICO_CONTRACT_ADDR, abiStr=EOS_ICO_CONTRACT_ABI)

        if not self.eosContract:
            return False

        return True

    def getEtherBalance(self, addr=None):
        '''
        Gets the ether balance of the given account.
        If not specified then this uses your account.
        '''
        if not self.eosContract:
            return None

        if not addr: 
            addr = self.myAddr

        return EthConnection.getEtherBalance(self, addr)

    def isClaimed(self, window, addr=None):
        '''
        Checks if the address claimed the eos on the window.
        If not specified then this uses your account.
        '''
        if not self.eosContract:
            return None

        if not addr: 
            addr = self.myAddr

        return bool(self.eosContract.call().claimed(window, addr))


    def getBought(self, window, addr=None):
        '''
        Gets the amount bought (in ether) by this address on this window.
        If not specified then this uses your account.
        '''
        if not self.eosContract:
            return None
        
        if not addr: 
            addr = self.myAddr

        ether = self.eosContract.call().userBuys(window, addr)
        return self.toEther(ether)

    
    def getTotalBought(self, window):
        '''
        Gets the total amount (in ether) bought by everyone on
        this window.
        '''
        if not self.eosContract:
            return None
        
        ether = self.eosContract.call().dailyTotals(window)
        return self.toEther(ether)

    def claimAllEstimateGas(self):
        '''
        Estimates the necessary gas for a claimAll() call.
        '''
        tx = self.initTransaction(self.myAddr)
        return self.eosContract.estimateGas(tx).claimAll()

    def claimAll(self, password, gas=None):
        '''
        Claims all the eos bought so far on any closed window.
        This will add a transaction on the blockchain, so your
        account needs to be added to the geth/parity node.
        '''
        if not self.eosContract:
            return None

        txHash = None
        try:
            if self.unlock(self.myAddr, password):
                tx = self.initTransaction(self.myAddr, gas=gas)
                txHash = self.eosContract.transact(tx).claimAll()
        finally:
            self.lock(self.myAddr)

        return txHash

    def claimEstimateGas(self, window):
        '''
        Estimates the necessary gas for a claim() call.
        '''
        tx = self.initTransaction(self.myAddr)
        return self.eosContract.estimateGas(tx).claim(window)

    def claim(self, window, password, gas=None):
        '''
        Claims all the eos bought on the window.
        This will add a transaction on the blockchain, so your
        account needs to be added to the geth/parity node.
        '''
        if not self.eosContract:
            return None

        txHash = None
        try:
            if self.unlock(self.myAddr, password):
                tx = self.initTransaction(self.myAddr, gas=gas)
                txHash = self.eosContract.transact(tx).claim(window)
        finally:
            self.lock(self.myAddr)

        return txHash

    def buyEstimateGas(self, ether):
        '''
        Estimates the necessary gas for a buy() call.
        '''
        tx = self.initTransaction(self.myAddr, toAddr=EOS_ICO_CONTRACT_ADDR, ether=ether)
        return self.web3.eth.estimateGas(tx)

    def buy(self, ether, password, gas=None):
        '''
        Uses the given amount ether to buy eos on the current open window.
        This will add a transaction on the blockchain, so your
        account needs to be added to the geth/parity node.
        '''
        if not self.eosContract:
            return None

        txHash = None
        try:
            if self.unlock(self.myAddr, password):
                txHash = self.sendTransaction(
                            self.myAddr,
                            EOS_ICO_CONTRACT_ADDR,
                            ether=ether,
                            gas=gas)
        finally:
            self.lock(self.myAddr)

        return txHash
    

def __test(addr, password):
    eos = EOSContract(addr)
    eos.connect()

    if eos.isConnected():
        print( "Claimed 6:", eos.isClaimed(6) )
        print( "Bought 0:", eos.getBought(0) )
        print( "Total 1:", eos.getTotalBought(1) )
        print( "Ether: ", eos.getEtherBalance())
        
        gas = eos.claimAllEstimateGas()
        print("Estimate gas for claimAll:", gas)

        print( "Claiming...")
        # calls with 1% more gas than the estimated
        #print(eos.claimAll(password, gas * 1.01)) 
        print( "Claimed!")

        gas = eos.buyEstimateGas(0.01)
        print ("Buy gas estimate", gas)
        print("Buying...")
        #eos.buy(0.0001, password)
        print( "Bought!")

