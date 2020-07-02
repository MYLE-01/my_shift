[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

# my shift
base on your work patten will work out if you on/off
even if you do days then nite like i do 2 days swing day then 2 nites then 4 days off :)

Big thanks to [mf-socials](https://github.com/mf-social/ps-date-countdown) for his countdown script 

that pointed me down down the track well where to start so thanks mf-socials again

Had the logic just did not know were to start 

first wrote it in vb that was easy

python still getting head around it

took me longer to write this readme than to write the code.

## How it works
This script creates a sensor that work out weather you are on/off for today
with a heap of attribute 



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
'holiday_start:' | True | string | Date, in format DD/MM/YYYY of holiday start
'holiday_end:' | True | string | Date, in format DD/MM/YYYY of holiday end

`patten:` is what shift patten are you doing
eg
DDNN = work 2 days then 2 nites

DDDDD = work 5 days in a row

`firstdayshift:` only has tobe full out once as it just uses maths to work out weather you on/off



shiftpatten | patten
--|--
'4x4x12'|    4 days ON x 4 days off x 12 hour days and it a 8 day cycle 
'4x2x12'|    4 days ON x 2 days off x 12 hour days and it a 6 day cycle
'5x2x8'|    5 days ON x 2 days off x 8 hour days and it a 7 day cycle
'6x1x8' |    6 days ON x 1 day off x 8 hour days and it a 7 day cycle


NOTE:

holiday_start: and holiday_end: will only kick in after next restart


must be small x

I have tested the above shiftpatten if someone has a differance patten it should work


if you are a monday-friday worker try this [workday Binary Sensor](https://www.home-assistant.io/integrations/workday/)
as this look at the public hoildays in your country

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
holiday_start: 26/05/2020
holiday_end: 12/07/2020
```
So, the sensor we created above would come out as:

```
icon: 'mdi:calendar-star'
friendly_name: StePhan's Roster
shift patten: 4x4x12
patten: DDNN
day_of_this_shift_patten: '2'
this_day: Day
next_start_date: 5/11/2019
First_Day_Shift_Was: 20/10/2019
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

## how I use in my house

As the alarm wakes me 2 day out of 8 day cycle

```
#=======================================================================
- id: 'Wake me up roster only morning'
  alias: Wake me up roster morning
  trigger:
  - at: '4:00:00'
    platform: time
  condition:
    condition: and
    conditions:
    - condition: state
      entity_id: sensor.stephan_4x4x12
      state: 'on'
    - condition: template
    # read the attributes of my sensor am I on DAYS/NIGHT of off
      value_template: >-
        {{states.sensor.stephan_4x4x12.attributes["this_day"] == 'Day'}}
  action:
  - data:
      entity_id: switch.kettle_power
    service: switch.turn_on
  - data:
      entity_id: light.his_side
    service: light.turn_on
  - delay: '00:10:00'
  - data:
      entity_id: light.his_side
    service: light.turn_off  
  ```
  and the afternoon one
  which as the bed sensor in the condition mite have got up
  
  ```
#=======================================================================
#
#=======================================================================
- id: 'Wake me up roster only afternoom'
  alias: Wake me up roster afternoom
  trigger:
  - at: '16:00:00'
    platform: time
  condition:
    condition: and
    conditions:
    - condition: state
      entity_id: sensor.stephan_4x2x12
      state: 'on'
    - condition: template
      value_template: >-
        {{states.sensor.stephan_4x4x12.attributes["this_day"] == 'Night'}}
    - condition: state
      entity_id: binary_sensor.in_bed_his_side
      state: 'on'
  action:
  - data:
      entity_id: switch.kettle_power
    service: switch.turn_on
  - data:
      entity_id: light.his_side
    service: light.turn_on
  - delay: '00:00:01'
  - data:
      entity_id: light.his_side
    service: light.turn_off   
  - delay: '00:00:01'
  - data:
      entity_id: light.his_side
    service: light.turn_on
  - delay: '00:00:01'
  - data:
      entity_id: light.his_side
    service: light.turn_off   
  - delay: '00:00:01'
  - data:
      entity_id: light.his_side
    service: light.turn_on
    ```




