#!/usr/bin/python3

import threading, datetime

cv = threading.Condition()
break_flag = False
refresh_time = []

def get_timeout():
  now = datetime.datetime.now()
  deadline = refresh_time[0]["expires"]
  return (deadline - now).total_seconds()


def add_refresh(id_str, expires_in):
  with cv:
    now = datetime.datetime.now()
    expires_in = datetime.timedelta(seconds=expires_in)
    refresh_time.append({"id": id_str, "expires": now + expires_in})
    refresh_time.sort(key=lambda x: x["expires"])
    cv.notify_all()

def set_break()
  with cv:
    break_flag = True
    cv.notify_all()

def get_id_to_refresh():
  with cv:
    while True:
      if break_flag:
        return None
      if len(refresh_time) > 0:
        t = get_timeout()
        if t > 0:
          cv.wait(timeout=t)
        else:
          break
      else:
        cv.wait()
    id_str = refresh_time[0]["id"]
    refresh_time = refresh_time[1:]
    return id_str
  return None
