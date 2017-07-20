from web3 import Web3, KeepAliveRPCProvider
from datetime import datetime
import os, sys, psutil

def getTimestamp():
    nowUTC = datetime.utcnow()
    return nowUTC.strftime('%Y-%m-%d %H:%M:%S')

running = True
percent = 0
memory = psutil.virtual_memory().percent

try:
    web3 = Web3(KeepAliveRPCProvider(host='eostracker.com', port='8545'))
    sync = web3.eth.syncing
    if sync:
        currentBlock = web3.eth.syncing.get('currentBlock', 0)
        highestBlock = web3.eth.syncing.get('highestBlock', 0)
        percent = 100 * currentBlock / highestBlock
    else:
        percent = 100
except:
    import traceback
    traceback.print_exc()
    percent = 0
    running = False

print('<html>\n')
print('<head><title> EOS Tracker </title></head>\n')
print('<h1> Parity Info </h1>\n')
print('<li><b> Parity Running: </b> %s\n' % str(running))
if running:
   print('<li><b> Sync Percentage: </b> %.2f %%\n' % percent)
print('<li><b> Memory Usage:</b> %.2f %%\n' % memory)
print('<li><b> Last Report: </b> %s UTC\n' % getTimestamp())
print('<br><br>\n<a href="../index.html">&lt;back</a>\n')
print('</html>')


