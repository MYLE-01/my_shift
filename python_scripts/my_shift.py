
today = datetime.datetime.now().date()

shiftpatten = data.get('shiftpatten')
name = data.get('name')
dateStr = data.get('firstdayshift')
patten = data.get('patten')

# Sort out the Date

dateSplit = dateStr.split("/")
dateDay = int(dateSplit[0])
dateMonth = int(dateSplit[1])
dateYear =  int(dateSplit[2])
FirstDayShift = datetime.date(dateYear,dateMonth,dateDay)

DaysDiff = ((today - FirstDayShift).days) + 1

PattenShift = shiftpatten.split("x")

WeekPatten = int(PattenShift[0]) + int(PattenShift[1])

shiftpatten = PattenShift[0] + "x" + PattenShift[1]+ "x" + PattenShift[2]

sensorName = "sensor.{}_{}".format(name.replace(" " , "_"),shiftpatten)

# now all we have to do is modulo which will give us a number between 0 and weekPatten

FirstDayShift_Mod = (DaysDiff % WeekPatten)

if (FirstDayShift_Mod == 0):
  FirstDayShift_Mod = WeekPatten


# work out the logic for on/off

# need to make patten longer with some blank
# so it dont error on days OFF
patten = patten + " " * FirstDayShift_Mod

ThisShift = ""
areweonoff = ""

if FirstDayShift_Mod > int(PattenShift[0]):
  areweonoff = 'Off'
  ThisShift = "OFF"

elif FirstDayShift_Mod <= int(PattenShift[0]):
  areweonoff = 'on'
  ThisShift = patten[FirstDayShift_Mod-1]

# well as we know what day patten we are in
# we can work out our next start date.
nextStartdays = (WeekPatten - FirstDayShift_Mod) 

nextstartDate = today + datetime.timedelta(nextStartdays + 1 )

nextoffDate = nextstartDate - datetime.timedelta(days=int(PattenShift[1]))

if nextoffDate < nextstartDate :
  nextoffDate = nextoffDate + datetime.timedelta(days=WeekPatten)

# hard work done put what we know into the sensor
# attributes So we can use them somewhere else in home assistant

# presence

hass.states.set(sensorName , areweonoff ,
  {
    "icon" : "mdi:calendar-star" ,
    "friendly_name" : "{}'s {}".format(name, "Roster") ,
    "shift patten" :"{}".format(shiftpatten) ,
    "patten" : "{}".format(patten.rstrip()) ,
    "day_of_this_shift_patten" : "{}".format(FirstDayShift_Mod) ,
    "this_day": "{}".format(ThisShift.replace("D","Day").replace("N","Night")),
    "next_start_date" : "{}/{}/{}".format(nextstartDate.day,nextstartDate.month,nextstartDate.year) , 
    "next_off_date" : "{}/{}/{}".format(nextoffDate.day,nextoffDate.month,nextoffDate.year) , 
    "First_Day_Shift_Was" : "{}/{}/{}".format(FirstDayShift.day,FirstDayShift.month,FirstDayShift.year)
  }
)

# this Is my first home assistant python Script 
# have no idea how the home assistant stuff works
# python heaps of help from google.
# the shift logic that was the easy bit.
