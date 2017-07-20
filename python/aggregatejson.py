import sys
import eosutils


if __name__ == '__main__':
    if len(sys.argv) > 1:
        window = int(sys.argv[1])
    else:
        window = eosutils.getCurrentWindow()

    print(window)

    delta = 1
    if len(sys.argv) > 2:
        delta = int(sys.argv[2])

    fileName = '/home/ubuntu/json/aggregated_window_%03d.json' % window

    eosutils.exportAggregatedJson(fileName, window, delta)

    print('Saved %s' % fileName)

