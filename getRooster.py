import datetime, random, urllib.request, time, re, json


def interpolate(inputValue, source, result):
    source = group(source,2)
    result = group(result,2)
    bundleList = []
    for src, res in zip(source, result):
        bundleList.append(Bundle(src[0], src[1], res[0],res[1]))
    output = []
    for bundle in bundleList:
        output.append(bundle.evaluate(inputValue))
        output = [x for x in output if x is not None]
    return output[0]

class Bundle():
    def __init__(self, start, end, start2, end2):
        self.inputRange = [start, end]
        self.outputRange = [start2, end2]
    def evaluate(self, value):
        if self.inputRange[0] <= value <= self.inputRange[1]:
            difference = self.inputRange[1] - self.inputRange[0]
            # print("the difference between input values is " + str(difference))
            value = value - self.inputRange[0]
            outputDifference = self.outputRange[1] - self.outputRange[0]
            # print("the difference between output values is " + str(outputDifference))
            part = value / difference
            # print(part)
            return (part * outputDifference) + self.outputRange[0]
        else:
            pass


def group(lst, n):
  for i in range(0, len(lst), n):
    val = lst[i:i+n]
    if len(val) == n:
      yield tuple(val)




# leerlingnummer = input()



items = ["startTime", "endTime", "dayOfWeek", "subject", "attendees", "location"]
def getLesson(leerlingnummer):
    try:
        website = urllib.request.urlopen("https://beta.rooster.hetmml.nl/get/s/"+leerlingnummer+".json")
        # time.sleep(1)
        siteContent = (website.read())
    except urllib.error.HTTPError:
        return ["error"]

    siteList = (str(siteContent)[2:-1])
    siteJSON = json.loads(siteList)


    # Manual overwrite
    currentTime = interpolate( float(datetime.datetime.now().hour) + float(datetime.datetime.now().minute/100),[0,8.30,8.30,9.45,9.45,10.45, 10.45, 12.15,12.15,13.15,13.15,14.45,14.45,15.45,15.45,17,17,24],[-1,-1,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7])
    # currentTime = interpolate(10.36,[8.20,9.35,9.35,10.35, 10.35, 12.05,12.05,13.05,13.05,14.35,14.35,15.35,15.5,17],[0,0,1,1,2,2,3,3,4,4,5,5,6,6])

    # Manual overwrite
    today = (datetime.datetime.today().weekday() + (currentTime == 7)) % 7
    # today = 2

    currentTime = currentTime - (currentTime == 7) * 8

    currentlesson = None
    nextlesson = None
    for subject in siteJSON:
        # print("currentTime is: " + str(currentTime))
        if subject["dayOfWeek"] == today:
            # datetime.
            # print( str(subject["startTime"]) + " at " + str(currentTime))
            if (subject["startTime"] <= currentTime) and (currentTime < subject["endTime"]):
                currentlesson = (subject)
                # print("found lesson")
            # Seeing if it is the next lesson
            nextTime = currentTime + 1.0
            if (subject["startTime"] <= nextTime) and (nextTime < subject["endTime"]):
                nextlesson = (subject)
                # print("found next lesson")
    # print(currentlesson)
    return [currentlesson, nextlesson]
    # print(siteJSON[0]["startTime"])
    # print(datetime.time.hour)
