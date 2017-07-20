import eosutils
from eoscontract import EOSContract

eos = EOSContract('0x21022d71ec014cf095381804675ffe17a039d015')
eos.connect()

if eos.isConnected():
    print( eos.getTotalBought( eosutils.getCurrentWindow() ) )