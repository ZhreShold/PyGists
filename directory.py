''' Directory related operations.'''

import os
import sys
import fnmatch

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

####################################
### list subdirs in root folder ###
def list_dir(root):
  return [x for x in os.listdir(root) if os.path.isdir(x)]
  
################################################
### list files with extension in root folder ###
def list_files_with_extension(root, ext):
  return [x for x in os.listdir(root) if os.path.isfile(x) and os.path.splitext(x)[1]==ext]

####################################################
### list files recursively with pattern to match ###
# py_files = list_files_recursive('.', '*.py')
def list_files_recursive(root, pattern):
  matches = []
  for root, dirnames, filenames in os.walk(root):
    for filename in fnmatch.filter(filenames, pattern):
      matches.append(os.path.join(root, filename))
