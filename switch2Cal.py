import os
# Gather input
if __name__ == '__main__':
  # find file
  inputFileName = os.path.expanduser(os.path.join('~', '.switch', 'switch_history'))

  # read the content into a set of unique lines
  formerProject = ''
  for line in open(inputFileName, 'r'):
    #remove trailing EOL and split by space
    tokens = line.rstrip('\r\n').split(' ')
    if len(tokens) == 2:
      timestamp, currentProject = tokens
    else:
      currentProject = False
    if currentProject != formerProject:
      print currentProject
      formerProject = currentProject

# Perform work
# Deliver results
# Handle failure
