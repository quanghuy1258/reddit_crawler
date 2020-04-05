#!/usr/bin/python3

import ipaddress, json

def try_string_to_int(s, default):
  try:
    return int(s)
  except:
    return default

def try_string_to_ipv4(s, default):
  try:
    return str(ipaddress.IPv4Address(s))
  except:
    return default

def print_config(config):
  print("="*36 + " CONFIG " + "="*36)
  print(json.dumps(config, indent=2))
  print("="*80)
