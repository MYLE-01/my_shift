
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

# work out the logic for on/off

# need to make patten longer with some blank
# so it dont error on days OFF
patten = patten + " " * FirstDayShift_Mod

ThisShift = ""

if FirstDayShift_Mod >= int(PattenShift[0]):
  areweonoff = 'Off'
  ThisShift = "OFF"

elif FirstDayShift_Mod < int(PattenShift[0]):
  areweonoff = 'on'
  ThisShift = patten[FirstDayShift_Mod-1]

# well as we know what day patten we are in
# we can work out our next start date.
nextStartdays = (WeekPatten - FirstDayShift_Mod) 

# to mines over this logic if its first day
# do we show todays date or next shift start

nextstartDate = today + datetime.timedelta(nextStartdays + 1 )

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
    "First_Day_Shift_Was" : "{}/{}/{}".format(FirstDayShift.day,FirstDayShift.month,FirstDayShift.year)
  }
)

# this Is my first home assistant python Script 
# have no idea how the home assistant stuff works
# python heaps of help from google.
# the shift logic that was the easy bit.
