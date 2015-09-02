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
  if sys.version_info[0:2] >= (3, 4):
      mkdir_34(path)
  elif sys.version_info[0:2] >= (2, 7):
      mkdir_27(path)
  else:
      print("At least python 2.7 required")
      raise 

####################################
### list subdirs in root folder ###
def list_dir(root):
  return [x for x in os.listdir(root) if os.path.isdir(os.path.join(root,x))]
  
################################################
### list files with extensions in root folder ###
def list_files_with_extension(root, exts):
  return [x for x in os.listdir(root) if os.path.isfile(os.path.join(root,x)) and os.path.splitext(x)[1] in exts]

####################################################
### list files recursively with patterns to match ###
# py_files = list_files_recursive('.', ['*.py', '*a.jpg','abc.*'])
def list_files_recursive(root, patterns):
    matches = set()
    for root, dirnames, filenames in os.walk(root):
        for pattern in patterns:
            for filename in fnmatch.filter(filenames, pattern):
                matches.add(os.path.join(root, filename))
    return matches
