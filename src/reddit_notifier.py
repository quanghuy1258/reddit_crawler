#!/usr/bin/python3

import threading, traceback

cv = threading.Condition()
break_flag = False
wait_time = 60

########################################
# DO SOMETHING HERE
########################################

def set_break():
  global break_flag
  with cv:
    break_flag = True
    cv.notify_all()

def get_notify(latest_config):
  with cv:
    cv.wait(timeout=wait_time)
    if break_flag:
      return None
    list_text = []
    try:
      ####################################
      # DO SOMETHING HERE
      ####################################
    except:
      list_text.append(traceback.format_exc())
    return list_text
  return None
