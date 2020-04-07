#!/usr/bin/python3

import src.check_libs
from src import load_config, utils, db, refresh_token, telegram_bot, reddit_notifier

import uuid, json, urllib.parse, requests, requests.auth, threading

config = load_config.get_config()
utils.print_config(config)

server_host = utils.try_string_to_ipv4(config["server"]["host"], "0.0.0.0")
server_port = utils.try_string_to_int(config["server"]["port"], 8080)

from flask import Flask, redirect, request
app = Flask(__name__)

@app.route("/ping")
def ping():
  return "OK"

@app.route(config["reddit"]["home_route"])
def reddit_home():
  state = str(uuid.uuid4())
  db.access_object(state)
  params = {}
  params["client_id"] = config["reddit"]["client_id"]
  params["response_type"] = "code"
  params["state"] = state
  params["redirect_uri"] = config["reddit"]["redirect_uri"]
  params["duration"] = config["reddit"]["duration"]
  params["scope"] = " ".join(config["reddit"]["scope"])
  url = "https://ssl.reddit.com/api/v1/authorize?" + urllib.parse.urlencode(params)
  return """
      <a href={}>Authenticate with reddit</a><br>
    """.format(url, state)

@app.route(config["reddit"]["redirect_route"])
def reddit_callback():
  ret = {}
  ret["error"] = request.args.get("error", "")
  ret["state"] = request.args.get("state", "")
  ret["code"] = request.args.get("code", "")
  if ret["code"]:
    client_auth = requests.auth.HTTPBasicAuth(config["reddit"]["client_id"], config["reddit"]["client_secret"])
    post_data = {"grant_type": "authorization_code",
                 "code": ret["code"],
                 "redirect_uri": config["reddit"]["redirect_uri"]}
    headers_data = {"user-agent": str(uuid.uuid4())}
    response = requests.post("https://ssl.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers_data)
    ret["token"] = response.json()
    if "access_token" in ret["token"]:
      db.write_key(ret["state"], "access_token", ret["token"]["access_token"])
    if "refresh_token" in ret["token"]:
      db.write_key(ret["state"], "refresh_token", ret["token"]["refresh_token"])
      refresh_token.add_refresh(ret["state"], ret["token"]["expires_in"])
  flag = True
  if ret["state"]:
    flag = db.callback(ret["state"], ret)
  else:
    flag = False
  if ret["error"]:
    return "ERROR: {}".format(ret["error"])
  if not flag:
    return "ERROR: Unknow state: {}".format(ret["state"])
  return redirect("https://www.reddit.com/")

def refresh_token_func():
  while True:
    id_str = refresh_token.get_id_to_refresh()
    if id_str is None:
      break
    token = db.read_key(id_str, "refresh_token")
    client_auth = requests.auth.HTTPBasicAuth(config["reddit"]["client_id"], config["reddit"]["client_secret"])
    post_data = {"grant_type": "refresh_token",
                 "refresh_token": token}
    headers_data = {"user-agent": str(uuid.uuid4())}
    response = requests.post("https://ssl.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers_data)
    ret = response.json()
    if "access_token" in ret:
      db.write_key(id_str, "access_token", ret["access_token"])
      refresh_token.add_refresh(id_str, ret["expires_in"])

def push_notify():
  bot = telegram_bot.TelegramBot(config["telegram"]["token"])
  chat_id = config["telegram"]["chat_id"]
  chat_id = utils.try_string_to_int(chat_id, chat_id)
  while True:
    list_text = reddit_notifier.get_notify(config)
    if list_text is None:
      break
    for text in list_text:
      bot.sendMessage(chat_id, text)

if __name__ == "__main__":
  refresh_token_thread = threading.Thread(target=refresh_token_func)
  refresh_token_thread.start()
  push_notify_thread = threading.Thread(target=push_notify)
  push_notify_thread.start()

  app.run(host=server_host, port=server_port)

  refresh_token.set_break()
  refresh_token_thread.join()
  reddit_notifier.set_break()
  push_notify_thread.join()
