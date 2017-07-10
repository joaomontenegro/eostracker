# @Copyright Joao Montenegro 2017

import sys
import eosutils

def usage():
    print("Usage: %s WINDOW [INTERVAL_MINUTES]" % sys.argv[0])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    window = int(sys.argv[1])

    delta = 1
    if len(sys.argv) > 2:
        delta = int(sys.argv[2])

    fileName = 'aggregated_window%03d.json' % window

    eosutils.exportAggregatedJson(fileName, window, delta)

    print('Saved %s' % fileName)
