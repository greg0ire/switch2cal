#!bin/python
import os
from collections import deque
from icalendar import Calendar, Event
from datetime import datetime
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
          'start_date': float(startTimestamp),
          'end_date': float(currentTimestamp)})

      startTimestamp  = currentTimestamp

    formerProject   = currentProject
    formerTimestamp = currentTimestamp

  # add last event
  events.append({
    'name': formerProject,
    'start_date': float(startTimestamp),
    'end_date': float(currentTimestamp)})

  # Perform work
  # Deliver results
  cal = Calendar()
  cal.add('prodid', '-//Generated with switch2cal//gparis//')
  cal.add('version', '2.0')
  for period in events:
    event = Event()
    event.add('summary', period['name'])
    event.add('dtstart', datetime.fromtimestamp(period['start_date']))
    event.add('dtend', datetime.fromtimestamp(period['end_date']))
    cal.add_component(event)

  f = open('/tmp/imputations.ics', 'wb')
  f.write(cal.as_string())
  f.close()
  # Handle failure
