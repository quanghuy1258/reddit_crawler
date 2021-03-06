#!/usr/bin/python3

import json, datetime, os.path, os

db_dir = "database/"

def get_time_str():
  return str(datetime.datetime.now())

def check_object_exists(id_str):
  return os.path.isfile(db_dir + id_str)

def list_objects():
  objects = []
  for f in os.listdir(db_dir):
    if f == ".gitignore":
      continue
    objects.append(f)
  return objects

def create_object(id_str):
  if check_object_exists(id_str):
    return
  data = {}
  data["id"] = id_str
  data["log"] = []
  data["log"].append({"time": get_time_str(), "event": "Create object"})
  data["callback"] = []
  with open(db_dir + id_str, "w") as f:
    json.dump(data, f, indent=2)

def access_object(id_str):
  if not check_object_exists(id_str):
    create_object(id_str)
  data = None
  with open(db_dir + id_str, "r") as f:
    data = json.load(f)
  data["log"].append({"time": get_time_str(), "event": "Access object"})
  with open(db_dir + id_str, "w") as f:
    json.dump(data, f, indent=2)

def callback(id_str, value):
  if not check_object_exists(id_str):
    return False
  data = None
  with open(db_dir + id_str, "r") as f:
    data = json.load(f)
  time_str = get_time_str()
  data["log"].append({"time": time_str, "event": "Callback"})
  data["callback"].append({"time": time_str, "value": value})
  with open(db_dir + id_str, "w") as f:
    json.dump(data, f, indent=2)
    return True
  return False

def write_key(id_str, key, value):
  if not check_object_exists(id_str):
    return False
  data = None
  with open(db_dir + id_str, "r") as f:
    data = json.load(f)
  data[key] = value
  with open(db_dir + id_str, "w") as f:
    json.dump(data, f, indent=2)
    return True
  return False

def read_key(id_str, key):
  if not check_object_exists(id_str):
    return None
  data = None
  with open(db_dir + id_str, "r") as f:
    data = json.load(f)
  if key in data:
    return data[key]
  return None

def read_object(id_str):
  if not check_object_exists(id_str):
    return None
  with open(db_dir + id_str, "r") as f:
    return json.load(f)
