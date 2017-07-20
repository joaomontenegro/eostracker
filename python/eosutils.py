import os, json
from datetime import (datetime, timedelta)

#### Window Date Time ####
def formatDatetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def parseDatetime(dtStr):
    return datetime.strptime(dtStr, '%Y-%m-%d %H:%M:%S')

def getNowUTC():
    return datetime.utcnow()

def getStartDatetime():
    return parseDatetime('2017-06-26 13:00:00')

def getWindowTimedelta(window):
    if window == 0:
        return timedelta(days=5)
    return timedelta(hours=23)

def getWindowStartDatetime(window):
    if window > 350 or window < 0:
        return None

    if window == 0:
        return getStartDatetime()

    windowTime = getStartDatetime()
    windowTime += timedelta(days=5)
    windowTime += timedelta(hours=23) * (window - 1)
    return windowTime

def getWindowOfUTC(dt):
    if dt < getStartDatetime():
        return None

    for i in range(1, 350):
        if dt < getWindowStartDatetime(i):
            return i - 1
    return None

def getCurrentWindow():
    return getWindowOfUTC(getNowUTC())


#### Window Json files ####
def getJsonDir():
    return os.environ.get('EOS_TRACKER_JSON_DIR', os.path.realpath('/home/ubuntu/json/'))

def getJsonFileForWindow(window):
    return os.path.join(getJsonDir(), 'window_%03d.json' % window)

def readJsonForWindow(window):
    with open(getJsonFileForWindow(window)) as jsonFile:
        data = json.load(jsonFile)
        return data


#### Json file aggregation ####
def __getSortedData(data):
    sortedData = []
    for (key, value) in data.items():
        dt = parseDatetime(key)
        sortedData.append((dt, value))

    return sorted(sortedData)


def aggregateJson(window, delta=1):
    data = readJsonForWindow(window)
    sortedData = __getSortedData(data)

    windowStart = getWindowStartDatetime(window)
    windowEnd = windowStart + getWindowTimedelta(window)

    intervals = []
    intervalStart = windowStart
    step = timedelta(minutes=delta)

    i = 0

    while intervalStart < windowEnd:
        intervalEnd = intervalStart + step

        values = []

        while True:
            if i >= len(sortedData):
                break;

            (dt, value) = sortedData[i]

            if dt < intervalStart:
                i += 1
                continue

            if dt >= intervalStart and dt < intervalEnd:
                values.append(value)
                i += 1
            else:
                break

        intervals.append( (intervalStart, values) )
        intervalStart = intervalEnd

    return intervals

def getJsonEmptyIntervals(window, delta=1):
    emptyIntervals = []
    for (dt, values) in aggregateJson(window, delta):
        if not values:
            emptyIntervals.append(dt)
    return emptyIntervals

def exportAggregatedJson(filepath, window, delta=1):
    with open(filepath, 'w') as jsonFile:
        intervalsDict = {}
        previous = 0

        for (dt, values) in aggregateJson(window, 1):
            if not values:
                maxValue = previous
            else:
                maxValue = max(values)

            intervalsDict[formatDatetime(dt)] = maxValue
            previous = maxValue

        data = json.dumps(intervalsDict, sort_keys=True)
        jsonFile.write(data)




def __testDatetime():
    now = getNowUTC()
    nowStr = formatDatetime(now)
    print(type(nowStr), nowStr)
    nowDate = parseDatetime(nowStr)
    print(type(nowDate), nowDate)

    print('current window: ', getCurrentWindow())


def __testAggregation():
    print("Aggregated:")
    for (dt, values) in aggregateJson(7, 1):
        print(formatDatetime(dt), values)

    print("Empty:")
    for dt in getJsonEmptyIntervals(7, 1):
        print(formatDatetime(dt))

    print("Saving aggregated_window_007.json")
    exportAggregatedJson("aggregated_window_007.json", 7, 1)

