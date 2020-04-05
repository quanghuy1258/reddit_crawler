#!/usr/bin/python3

import json, os

config_file = "config/config.json"
config_file = os.path.abspath(config_file)

def get_config():
  if not os.path.isfile(config_file):
    print("ERROR: File {} Not found".format(config_file))
    exit(1)
  try:
    config = json.load(open(config_file))
    return config
  except:
    print("ERROR: File {} Is not JSON".format(config_file))
    exit(1)
