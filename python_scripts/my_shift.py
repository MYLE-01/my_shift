

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

# Work out Days diff
DaysDiff = (today - FirstDayShift).days

#Split the Shift pattens
PattenShift = shiftpatten.split("x")

#by adding PattenShift[0] + PattenShift[1] we know how long a shift patten is
WeekPatten = int(PattenShift[0]) + int(PattenShift[1])

# know all we have to do is modulo  which will give us a number between 0 and weekPatten
FirstDayShift_Mod = (DaysDiff % WeekPatten)

# work out the logic for on/off

if FirstDayShift_Mod >= int(PattenShift[0]):
  areweonoff = 'Off'
elif FirstDayShift_Mod < int(PattenShift[0]):
  areweonoff = 'on'

# well as we know what day patten we are in
# we can work out our next start date.
nextStartdays = WeekPatten - FirstDayShift_Mod

nextstartDate = today + datetime.timedelta(nextStartdays)

#hard work done put what we know into the sensor

hass.states.set(sensorName , areweonoff ,
  {
    "icon" : "mdi:calendar-star" ,
    "friendly_name" : "{}'s {}".format(name, shiftpatten) ,
    "dayspatten" : "{}".format(FirstDayShift_Mod) ,
    "nextstartdate" : "{}/{}/{}".format(nextstartDate.day,nextstartDate.month,nextstartDate.year)
  }
)

# this Is my first home assistant python Script 
# have no idea how the home assistant stuff works
# python heaps of help from google.
# the shift logic that was the easy bit.
