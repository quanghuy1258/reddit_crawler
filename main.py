#!/usr/bin/python3

import src.check_libs
from src import load_config, utils, db

from uuid import uuid4
import json, urllib.parse, requests, requests.auth

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
  state = str(uuid4())
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
    headers_data = {"user-agent": str(uuid4())}
    response = requests.post("https://ssl.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers_data)
    ret["token"] = response.json()
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

if __name__ == "__main__":
  app.run(host=server_host, port=server_port)
