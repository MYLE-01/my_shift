# my shift
base on your work patten will work out if you on/off

Big thanks to [mf-socials](https://github.com/mf-social/ps-date-countdown) for his countdown script that show me how to write this python version I first wrote it about 5 year ago in a execl file


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
`patten:` | True | string | What the Patten DDNN = (doing 2 days then 2 nigths)

`patten:` is what shift patten are you doing

DDNN = work 2 days then 2 nites

DDDDD = work 5 days in a row

`firstdayshift:` only has tobe full out once as it just uses maths to work out weather you on/off


shiftpatten | patten
--|--
'4x4x12'|    4 days ON x 4 days off x 12 hour days 
'5x2x8'|    5 days ON x 2 days off x 8 hour days 
'6x1x8' |    6 days ON x 1 day off x 8 hour days 

## Usage
Each sensor **requires**:

```
name: NAME_OF_SHIFT_PATTEN
shiftpatten: SHIFT_PATTEN 4x4x12
patten: DDNN
firstdayshift: DD/MM/YYYY_date of first day of the patten must be sometime in the pass
```

examples:

```
name: StePhan
shiftpatten: 4x4x12
patten: DDNN
firstdayshift: 20/10/2019
```
So, the sensor we created above would come out as:

```
sensor.StePhan_4x4x12
friendly_name: StePhan's 4x4x12
state: on = working  off = notworking
dayspatten: what patten are we in
thisday: what shift are we working today
nextstartdate: next startof shift patten
```
## Example configuration.yaml entry
An example automation to create and refresh the above two sensors daily would be:

```yaml
automation:
  - alias: set the shift patten on/off
    trigger:
      - platform: time
        at: '00:00:01'
      - platform: homeassistant
        event: start
    action:
      - service: python_script.my_shift
        data:
          name: StePhan
          shiftpatten: 4x4x12
          patten: DDNN
          firstdayshift: 20/10/2019
```
## Showing it in lovelace
An example for lovelace
(at this point of time you have to the secondaryinfo-entity-row )

```
  - entity: sensor.stephan_4x4x12
    secondary_info: ' Next start: [[ {entity}.attributes.nextstartdate ]]''
    type: 'custom:secondaryinfo-entity-row'
```
next start date will show in secondary_info line
