# @Copyright Joao Montenegro 2017

from web3 import Web3, KeepAliveRPCProvider, IPCProvider
import json, time, os
from datetime import datetime

OUT_FILE_PREFIX = "%s/json/window" % os.environ.get("EOS_TRACKER_HOME", "/home/ubuntu")

def getFloat(value):
    '''
    Float values in ethereum are represented by integers
    that need to be devided by 10^18
    '''
    return value  / 1000000000000000000 


def getWindowTotal():
    try:
        # Connect
        web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))

        # EOS ICO contract's address and the ABI
        addr = '0xd0a6E6C54DbC68Db5db3A091B171A77407Ff7ccf'
        abi = json.loads('[{"constant":true,"inputs":[{"name":"","type":"uint256"},{"name":"","type":"address"}],"name":"claimed","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"owner_","type":"address"}],"name":"setOwner","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"time","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint128"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"foundersAllocation","outputs":[{"name":"","type":"uint128"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"day","type":"uint256"}],"name":"claim","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"foundersKey","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"},{"name":"","type":"address"}],"name":"userBuys","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"day","type":"uint256"}],"name":"createOnDay","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"freeze","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"keys","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"startTime","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"authority_","type":"address"}],"name":"setAuthority","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"dailyTotals","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"buy","outputs":[],"payable":true,"type":"function"},{"constant":true,"inputs":[],"name":"openTime","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"EOS","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"today","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"authority","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"eos","type":"address"}],"name":"initialize","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"createFirstDay","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"claimAll","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"timestamp","type":"uint256"}],"name":"dayFor","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"day","type":"uint256"},{"name":"limit","type":"uint256"}],"name":"buyWithLimit","outputs":[],"payable":true,"type":"function"},{"constant":false,"inputs":[],"name":"collect","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"numberOfDays","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"key","type":"string"}],"name":"register","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"createPerDay","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"inputs":[{"name":"_numberOfDays","type":"uint256"},{"name":"_totalSupply","type":"uint128"},{"name":"_openTime","type":"uint256"},{"name":"_startTime","type":"uint256"},{"name":"_foundersAllocation","type":"uint128"},{"name":"_foundersKey","type":"string"}],"payable":false,"type":"constructor"},{"payable":true,"type":"fallback"},{"anonymous":false,"inputs":[{"indexed":false,"name":"window","type":"uint256"},{"indexed":false,"name":"user","type":"address"},{"indexed":false,"name":"amount","type":"uint256"}],"name":"LogBuy","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"window","type":"uint256"},{"indexed":false,"name":"user","type":"address"},{"indexed":false,"name":"amount","type":"uint256"}],"name":"LogClaim","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"user","type":"address"},{"indexed":false,"name":"key","type":"string"}],"name":"LogRegister","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"LogCollect","type":"event"},{"anonymous":false,"inputs":[],"name":"LogFreeze","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"authority","type":"address"}],"name":"LogSetAuthority","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"}],"name":"LogSetOwner","type":"event"}]')

        # Get the contract
        contract = web3.eth.contract(abi, addr)

        # Get the Window for right now
        window = contract.call().today()

        # Get the total purchases on this window
        totalEOS = getFloat(contract.call().dailyTotals(window))
    except:
        import traceback
        traceback.print_exc()
        window = -1
        totalEOS = -1

    return window, totalEOS


def getTimestamp():
    nowUTC = datetime.utcnow()
    return nowUTC.strftime('%Y-%m-%d %H:%M:%S')


def writeToFile(line, window):

    filePath = "%s_%03d.json" % (OUT_FILE_PREFIX, window)

    with open(filePath, "a+") as outFile:
        # Get the position of the last character
        outFile.seek(0, os.SEEK_END)
        pos = outFile.tell()

        if pos == 0:
            # Add the first '{' if the file is empty
            line = '{\n%s' % line
        else:
            # Remove the last '}'
            while pos > 0 and outFile.read(1) != '\n':
                pos -= 1
                outFile.seek(pos, os.SEEK_SET)
            pos -= 1
            if pos > 0:
                outFile.seek(pos, os.SEEK_SET)
                outFile.truncate()      

            # Add a comma to the previous line
            line = ',\n%s' % line

        # Write line
        outFile.write(line)

        # Append the final '}'
        outFile.write("\n}")

window, totalEos = getWindowTotal()

if window != -1 and totalEos != -1:
    line = '    "%s": %f' % (getTimestamp(), totalEos)
    writeToFile(line, window)
    print(line)

