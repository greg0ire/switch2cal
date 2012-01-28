#!bin/python
import os
import time

from collections import deque
from icalendar import Calendar, Event
from datetime import datetime, timedelta
# Gather input
if __name__ == '__main__':
  # find file
  inputFileName = os.path.expanduser(os.path.join('~', '.switch', 'switch_history'))
  events        = deque([])

  # read the content into a set of unique lines
  formerProject   = ''
  formerTimestamp = ''
  startTimestamp  = ''
  for line in open(inputFileName, 'r'):
    # Parse the line
    # remove trailing EOL and split by space
    tokens = line.rstrip('\r\n').split(' ')
    if len(tokens) == 2:
      currentTimestamp, currentProject = tokens
    else:
      currentProject = ''

    if currentProject != formerProject:
      if formerProject != '':
        # got something to store
        events.append({
          'name': formerProject,
          'start_date': datetime.fromtimestamp(float(startTimestamp)),
          'end_date': datetime.fromtimestamp(float(currentTimestamp))})

      startTimestamp  = currentTimestamp

    formerProject   = currentProject
    formerTimestamp = currentTimestamp

  # add last event
  events.append({
    'name': formerProject,
    'start_date': datetime.fromtimestamp(float(startTimestamp)),
    'end_date': datetime.now()})

  # Perform work

  cleanedEvents = deque([])
  for period in events:
    # if a period is inside the work period, do not touch it
    # if it is outside, don't take it into account
    # if it overlapses, round the start_date to the nearest work period start
    startTime    = period['start_date']
    stopTime     = period['end_date']
    # validate events
    if startTime > stopTime:
      raise Exception("Event %s is invalid: %r > %r" % (period['name'], period['start_date'], period['end_date']))

    if startTime < stopTime:
      # compute the intersection of the event with working hours
      workStartTime = startTime.replace(hour=19, minute=30)
      workStopTime  = startTime.replace(hour=23, minute=59)

      # discard not intersecting events
      if not (workStopTime < startTime < stopTime < workStartTime + timedelta(days=1)):
        if startTime < workStartTime:
          cleanedStartTime = workStartTime
        elif startTime < workStopTime:
          cleanedStartTime = startTime
        else:
          cleanedStartTime = workStartTime + timedelta(days=1)

        if stopTime < workStopTime:
          cleanedStopTime = stopTime
        else:
          cleanedStopTime = workStopTime

        cleanedEvents.append({
          'name': period['name'],
          'start_date': cleanedStartTime,
          'end_date': cleanedStopTime})


  # Deliver results
  cal = Calendar()
  cal.add('prodid', '-//Generated with switch2cal//gparis//')
  cal.add('version', '2.0')
  for period in cleanedEvents:
    event = Event()
    event.add('summary', period['name'])
    event.add('dtstart', period['start_date'])
    event.add('dtend', period['end_date'])
    cal.add_component(event)

  f = open('/tmp/imputations.ics', 'wb')
  f.write(cal.as_string())
  f.close()
  # Handle failure
