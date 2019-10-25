# my shift
base on your work patten will work out if you on/off

## How it works
This script creates a sensor that work out weather you are on/off for today

Requires `python_script:` to be enabled in you configuration

## Installation
Copy the Python script in to your `/config/python_scripts`

## Script arguments
key | required | type | description
-- | -- | -- | --
`name:` | True | string | Name of the date (eg. StePhan)
`shiftpatten:` | True | string | Type of Shift  
`firstdayshift:` | True | string | Date, in format DD/MM/YYYY day 1 of shift patten

shiftpatten | patten
--|--
'4x4x12'|    4 days ON x 4 days off x 12 hour days 
'5x2x8'|    5 days ON x 2 days off x 8 hour days 
'6x1x8' |    6 days ON x 1 day off x 8 hour days 
