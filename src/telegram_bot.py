#!/usr/bin/python3

import requests

class TelegramBot:
  form = "https://api.telegram.org/bot{}/{}"

  def __init__(self, token):
    self.token = token

  def getMe(self):
    response = requests.get(self.form.format(self.token, "getMe"))
    return response.json()

  def getUpdates(self):
    response = requests.get(self.form.format(self.token, "getUpdates"))
    return response.json()

  def getAllMessages(self, chat_id=[]):
    ret = self.getUpdates()
    if not ret["ok"]:
      return ret
    ret["result"] = [update for update in ret["result"] if ("message" in update) and ((len(chat_id)) == 0 or (update["message"]["chat"]["id"] in chat_id))]
    return ret

  def sendMessage(self, chat_id, text):
    params = {
        "chat_id": chat_id,
        "text": text
      }
    response = requests.get(self.form.format(self.token, "sendMessage"), params=params)
    return response.json()

  def editMessageText(self, chat_id, message_id, text):
    params = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text
      }
    response = requests.get(self.form.format(self.token, "editMessageText"), params=params)
    return response.json()

  def deleteMessage(self, chat_id, message_id):
    params = {
        "chat_id": chat_id,
        "message_id": message_id
      }
    response = requests.get(self.form.format(self.token, "deleteMessage"), params=params)
    return response.json()
