import datetime, random, urllib.request, time, re, json

# Every set of two live times as input will be converted to the values in the second list
lessonTimes = [[0,8.30,8.30,9.45,9.45,10.45, 10.45, 12.15,12.15,13.15,13.15,14.45,14.45,15.45,15.45,17,17,24],[-1,-1,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7]]

# Interpolation code included, see https://docs.scipy.org/doc/scipy-0.19.1/reference/generated/scipy.interpolate.interp1d.html for docs
# Only the normal interpolation is implemented, no fancy args.
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

# End of interpolation code


# Using urllib to retrieve Json data from the schedule page online
def retrieveData(lln):
    try:
        website = urllib.request.urlopen("https://beta.rooster.hetmml.nl/get/s/"+lln+".json")
        # time.sleep(1)
        siteContent = (website.read())
    except urllib.error.HTTPError:
        return ["error"]

    siteList = (str(siteContent)[2:-1])
    result = json.loads(siteList)
    return result

def getScheduleTime():
    global lessonTimes
    now = datetime.datetime.now()
    liveTime = float(now.hour) + float(now.minute/100)
    lessonTime = interpolate( liveTime, lessonTimes[0], lessonTimes[1])
    return lessonTime

def getTime():
    result = {}
    weekday = datetime.datetime.today().weekday()
    lesson = getScheduleTime()
    # Since we want to say something about monday when asking sunday, we have to adjust if nesicarry
    result["day"] = (weekday + (lesson == 7)) % 7
    # If we are past the current day, ask the first hour of the next day
    # Since this function only handles the time, we just want to return -1
    result["hour"] = lesson - (lesson == 7) * 8
    return result


# items = ["startTime", "endTime", "dayOfWeek", "subject", "attendees", "location"]
def getLesson(leerlingnummer):

    scheduleData = retrieveData(leerlingnummer)

    scheduleTime = getTime()
    retrieveDay = scheduleTime["day"]
    retrieveHour = scheduleTime["hour"]

    nextLessons = [None, None]
    for subject in scheduleData:
        if subject["dayOfWeek"] == retrieveDay:
            if (subject["startTime"] <= retrieveHour) and (retrieveHour < subject["endTime"]):
                nextLessons[0] = subject
            nextTime = retrieveHour + 1.0
            if (subject["startTime"] <= nextTime) and (nextTime < subject["endTime"]):
                nextLessons[1] = subject
    return nextLessons

def getDay(leerlingnummer):
    scheduleData = retrieveData(leerlingnummer)

    scheduleTime = getTime()
    retrieveDay = scheduleTime["day"]

    nextLessons = []
    for subject in scheduleData:
        if subject["dayOfWeek"] == retrieveDay:
            currentLessons.append(subject)
    #TODO: order lessons
    return nextLessons

def getWeek(leerlingnummer):
    scheduleData = retrieveData(leerlingnummer)
    rooster = [[],[],[],[],[]]
    for subject in scheduleData:
        rooster[subject["dayOfWeek"]].append(subject)
    #TODO: order lessons
    return scheduleData
