import config, requests

class RachelMessage:
  def __init__(self, message_json):
    try:
      self.text = message_json['text']
    except KeyError:
      self.text = None
    self.chat_id = message_json['chat']['id']
    self.sender = {'first': message_json['from']['first_name'],
             'last': message_json['from']['last_name']}

  def reply(self, text):
    """ 
    Send a reply to a RachelMessage with given text
    Can be called on text = None, in which case no message will be sent
    """
    if text:
      r = requests.get(config.REQUEST_URL + \
      'sendMessage?chat_id=' + str(self.chat_id) + "&text=" + text)

  def reply_with_photo(self, filename):
    if filename:
      r = requests.post(config.REQUEST_URL + \
      'sendDocument?chat_id=' + str(self.chat_id), files={'document': open(config.FILE_PATH + filename, 'rb')})
    else:
      self.reply("Can't find anything for '" + self.text + "'. Sorry. ")