

today = datetime.datetime.now().date()

#read the Data in

shiftpatten = data.get('shiftpatten')
name = data.get('name')
dateStr = data.get('firstdayshift')
sensorName = "sensor.{}_{}".format(name.replace(" " , "_"),shiftpatten)

# Sort out the Date
dateSplit = dateStr.split("/")
dateDay = int(dateSplit[0])
dateMonth = int(dateSplit[1])
dateYear =  int(dateSplit[2])
FirstDayShift = datetime.date(dateYear,dateMonth,dateDay)

# Work out Days
DaysDiff = (today - FirstDayShift).days

PattenShift = shiftpatten.split("x")

WeekPatten = int(PattenShift[0]) + int(PattenShift[1])

FirstDayShift_Mod = (DaysDiff % WeekPatten)

# are we ON/OFF

if FirstDayShift_Mod >= int(PattenShift[0]):
  areweonoff = 'Off'
elif FirstDayShift_Mod < int(PattenShift[0]):
  areweonoff = 'on'

# we can work next Start Date

nextStartdays = WeekPatten - FirstDayShift_Mod

nextstartDate = today + datetime.timedelta(nextStartdays)

hass.states.set(sensorName , areweonoff ,
  {
    "icon" : "mdi:calendar-star" ,
    "friendly_name" : "{}'s {}".format(name, shiftpatten) ,
    "dayspatten" : "{}".format(FirstDayShift_Mod) ,
    "nextstartdate" : "{}/{}/{}".format(nextstartDate.day,nextstartDate.month,nextstartDate.year)
  }
)
