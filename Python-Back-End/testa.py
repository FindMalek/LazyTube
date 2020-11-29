from datetime import date, datetime, timedelta 
import re


f= ['PT2M43S', 'PT1H13S', 'PT1M42S', 'PT3M14S', 'PT1M46S', 'PT1M41S', 'PT2M45S', 'PT2M26S', 'PT1M39S', 'PT2M19S', 'PT2M45S', 'PT1M58S', 'PT3M52S', 'PT2M9S', 'PT1M54S', 'PT1M56S', 'PT2M34S']
minutes_patter = re.compile(r"(\d+)M")
hours_patter = re.compile(r"(\d+)H")
seconds_pattern = re.compile(r"(\d+)S")

for duration in f:
    hours = hours_patter.search(duration)
    minutes = minutes_patter.search(duration)
    seconds = seconds_pattern.search(duration)


    minutes = minutes.group(1) if minutes else "00"
    seconds = seconds.group(1) if seconds else "00"
    hours = hours.group(1) if hours else ""
    if(hours != ""):
        hours += ":"
    dur = str(hours)+str(minutes).zfill(2)+":"+str(seconds).zfill(2)
    print(dur)
#print(datetime.strptime(k, 'PT%M:%S.%f'))
