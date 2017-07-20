import sys
import traceback
import krakenex
import eoscontract
import eosutils
import logging

logging.basicConfig(level=logging.INFO,
    format='[EOSBOT] %(asctime)s (line %(lineno)d) [%(levelname)s]:\n*\t%(message)s\n')
log = logging.getLogger("EOSBot")

# Parameters
SECONDS_BEFORE_WINDOW_END = 60 * 5 * 60 * 12
ETHEREUM_NODE_HOST = "eostracker.com"
ETHEREUM_NODE_PORT = "8545"
PRICE_THRESHOLD = 0.1
AMOUNT_TO_BUY = 0.001 # in ether

##### TODO: move to command line arguments? Shouldn't be hardcoded
ETHEREUM_ADDRESS = "0x21022d71ec014cf095381804675ffe17a039d015"
KRAKEN_KEY_FILE_PATH = "kraken.key"
########################################

class EOSBot:
    def __init__(self, etherAddr, krakenKey, host='localhost', port='8545'):
        self.__isConnected = False
        self.currentWindow = eosutils.getCurrentWindow()

        # Connect to Ethereum
        try:
            self.eosContract = eoscontract.EOSContract(etherAddr, host, port)
            self.eosContract.connect()
            if self.eosContract.isConnected():
                log.info('Connection to Ethereum successful.')
                self.__isConnected = True
            else:
                log.error("Error connecting to Ethereum node.")
                return
        except:
            self.__isConnected = False
            log.error("Error connecting to Ethereum.")
            traceback.print_exc()
            return

        # Connect to EOS
        try:
            self.kraken = krakenex.API()
            self.kraken.load_key(krakenKey)
            self.krakenConn = krakenex.Connection()
            log.info('Connection to Kraken successful.')
        except:
            self.__isConnected = False
            log.error("Error connecting to Kraken.")
            return


    def __del__(self):
        self.krakenConn.close()


    def isConnected(self):
        return self.__isConnected

    def isOkToBuy(self, secondsBefore, amountEther, priceThreshold):
        if not self.isTimeOk(secondsBefore):
            log.warning("Not the right time yet.")
            return False

        etherBalance = self.getEtherBalance()
        if etherBalance is not None and etherBalance < amountEther:
            log.warning("Not enough ether balance: %f eth < %f eth" % (
                etherBalance, amountEther))
            return False
        elif etherBalance is None:
            return False

        if not self.isPriceOk(priceThreshold):
            return False

        log.info('Ok to Buy!')
        return True


    def isTimeOk(self, secondsBefore):
        windowEndTime = eosutils.getWindowStartDatetime(self.currentWindow + 1)
        now = eosutils.getNowUTC()
        delta = windowEndTime - now
        return (delta.days == 0
                and delta.seconds <= secondsBefore
                and delta.seconds >= 0)


    def isPriceOk(self, priceThreshold):
        icoPrice = self.getIcoPrice()
        if icoPrice is None:
            return False

        krakenPrice = self.getKrakenPrice()
        if krakenPrice is None:
            return False

        log.info("Prices: ICO: %f eth  |  Kraken: %f eth " % (
            icoPrice, krakenPrice))

        priceDiff = krakenPrice - icoPrice
        if priceDiff < 0:
            log.warning("ICO is more expensive than Kraken")
            return False

        ratio = priceDiff / icoPrice
        if ratio < priceThreshold:
            log.warning("Price Ratio below threshold: %f < %f)" % (
                ratio, priceThreshold))
            return False

        return True


    def getIcoPrice(self):
        total = self.eosContract.getTotalBought(self.currentWindow)
        if total is None:
            log.error("ICO Price: no result from query")

        return float(total) / 2000000


    def getKrakenPrice(self):
        queryResult = self.kraken.query_public('Ticker', {'pair':'EOSETH'},
            conn=self.krakenConn)

        error = queryResult.get('error', None)
        if error:
            log.error("Kraken Ticker: ", error)
            return None
        
        ticker = queryResult.get('result', {}).get('EOSETH', {}).get('c', [])
        if len(ticker) != 2:
            log.error("Kraken Ticker: no result")
            return None

        return float(ticker[0])


    def getKrakenBalance(self, coin='EOS'):
        queryResult = self.kraken.query_private('Balance', conn=self.krakenConn)

        error = queryResult.get('error', None)
        if error:
            log.error("Kraken Balance: ", error)
            return None

        balance = queryResult.get('result', {}).get(coin, None)
        if balance  is None:
            log.error("Kraken Balance: no result from query")
            return None

        return float(balance)


    def getIcoBalance(self):
        balance = self.eosContract.getBought(self.currentWindow)
        if balance is None:
            log.error("ICO Ether Balance: no result from query")
            return None

        return float(balance)

    def getEtherBalance(self):
        balance = self.eosContract.getEtherBalance()
        if balance is None:
            log.error("Ether Balance: no result from query")
            return None

        return float(balance)


    def buyEosOnIco(self, amountEther):
        # buy
        # wait for transaction (maybe all of these in separate functions)
        # wait for end of window
        # claim
        pass


    def sellEosOnKraken(self, amountEos):
        # Sell EoS
        pass


    def transferEosToKraken(self, krakenEOSAddress):
        # transfer EOS to kraken (need to add EOS ERC 20 contract to eoscontract)
        # wait for transaction (maybe in a different func?)
        pass


    def transferToEtherAddress(self):
        # transfer eth from kraken to ether address
        # wait for transaction (maybe in a different func?)
        pass

    def process(self, secondsBefore, amountEther, priceThreshold):
        pass
        '''
        #TODO: Pseudocode: do not call this

        if not self.isOkToBuy(secondsBefore, amountEther, priceThreshold):
            return

        log.info('About to buy!') # add more info

        tx = self.buyEosOnIco(amountEther)
        if not tx: return
        self.waitForTransaction(tx) # raise exception on timeout?

        waitForWindowToEnd()

        endOfWindowPrice = getIcoPrice()

        tx = self.claimAll()
        if not tx: return
        self.waitForTransaction(tx)

        tx = self.transferEosToKraken()
        if not tx: return
        self.waitForTransaction(tx)
        self.waitForTransactionOnKraken(tx) # TODO: maybe this needs different args
        amountEos = ??? get from kraken

        krakenPrice = self.getKrakenPrice()
        if krakenPrice is None:
            return False
        
        # Check the price again
        if not self.isPriceOk():
            return
        
        tx = self.sellEosOnKraken(amountEos)
        self.waitForTransactionOnKraken(tx)
        finalAmountEth = ??? get from Kraken

        # Calculate the profit
        profitEth = finalAmountEth - amountEther

        log.info('Success!! Transactioned: %f eos  |  Profit: %f eth ' % (
            amountEos, profitEth))
        '''

if __name__ == '__main__':
    bot = EOSBot(ETHEREUM_ADDRESS, KRAKEN_KEY_FILE_PATH,
        host=ETHEREUM_NODE_HOST, port=ETHEREUM_NODE_PORT)

    if not bot.isConnected():
        sys.exit(1)

    if bot.isOkToBuy(SECONDS_BEFORE_WINDOW_END, AMOUNT_TO_BUY, PRICE_THRESHOLD):
        print('Kraken balance: %f eos' % bot.getKrakenBalance('EOS'))
        print('Kraken balance: %f eth' % bot.getKrakenBalance('XETH'))
        print('ICO balance: %f eth' % bot.getIcoBalance())
        print('Ether balance: %f eth' % bot.getEtherBalance())