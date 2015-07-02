''' Directory related operations.'''

import os

### create directory if not exist ###

# python 2.7
def mkdir_2(path):
  try: 
      os.makedirs(path)
  except OSError:
      if not os.path.isdir(path):
          raise
          
          
# python 3.4
def mkdir_3(path):
  os.makedirs(path, exist_ok=True)
  
