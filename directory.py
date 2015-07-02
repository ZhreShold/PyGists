''' Directory related operations.'''

import os
import sys

#######################################
### create directory if not exist ###

# python 2.7
def mkdir_27(path):
  try: 
      os.makedirs(path)
  except OSError:
      if not os.path.isdir(path):
          raise
          
# python 3.4
def mkdir_34(path):
  os.makedirs(path, exist_ok=True)
  
# wrapper
def mkdir(path):
  if sys.version_info[0:2] >= (3, 4)
      mkdir_34(path)
  elif sys.version_info[0:2] >= (2, 7)
      mkdir_27(path)
  else:
      print("At least python 2.7 required")
      raise 
