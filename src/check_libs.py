#!/usr/bin/python3

import importlib

libs = []
libs.append("flask")

missing_libs = []

for lib in libs:
  if importlib.find_loader(lib) is None:
    missing_libs.append(lib)

if len(missing_libs) > 0:
  print("ERROR: Please install these libraries:")
  print("\t{}".format(", ".join(missing_libs)))
  print("HOW TO FIX:")
  for lib in missing_libs:
    print("\t$ pip3 install {}".format(lib))
  exit(1)
