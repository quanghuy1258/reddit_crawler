#!/usr/bin/python3

import requests, uuid

def create_headers(access_token):
  return {
      "Authorization": "bearer " + access_token,
      "user-agent": str(uuid.uuid4())
    }

def get_username(access_token):
  headers = create_headers(access_token)
  response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
  return response.json()['name']

def get_scopes(access_token, scopes=[]):
  headers = create_headers(access_token)
  params = {}
  if len(scopes) > 0:
    params["scopes"] = " ".join(scopes)
  response = requests.get("https://oauth.reddit.com/api/v1/scopes", headers=headers, params=params)
  return response.json()

def check_username_available(access_token, username):
  headers = create_headers(access_token)
  params = {"user": username}
  response = requests.get("https://oauth.reddit.com/api/username_available", headers=headers, params=params)
  return response.json()

def read_new(access_token, subreddit="", limit=1, select_field=["subreddit", "selftext", "title", "link_flair_text", "permalink", "url"]):
  headers = create_headers(access_token)
  params = {"limit": limit}
  response = requests.get("https://oauth.reddit.com{}/new".format("/r/" + subreddit if subreddit else ""), headers=headers, params=params)
  ret = response.json()
  if len(select_field) > 0:
    for i in range(limit):
      temp_dict = ret["data"]["children"][i]["data"]
      ret["data"]["children"][i]["data"] = {k: temp_dict[k] for k in select_field if k in temp_dict}
  return ret
