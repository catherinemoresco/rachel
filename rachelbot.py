import requests, time, re, random, config
from models.message import RachelMessage
import plugins.gif

class RachelBot:
  def __init__(self, token):
    self.offset = 0

  def get_updates(self):
    try:
      r = requests.get(config.REQUEST_URL+ \
             'getUpdates?offset=' + str(self.offset))
    except:
      time.sleep(5)
      return

    for result in r.json()['result']:
      self.offset = result['update_id'] + 1
      if result['message']:
          message = RachelMessage(result['message'])
          self.process(message)

  def process(self, message):
    message_text = message.text.split('/Rachel')[-1]
    print "Processing message: '" + message_text + "'"
    # Check for greeting
    match = re.search(r'\b(hello|hey|hi)\b', message_text, re.IGNORECASE)
    if match:
      message.reply(self.greet(message.sender['first']))
    # Check for a giphy search
    match = re.search('gif', message_text, re.IGNORECASE)
    if match:
      message.reply_with_photo(plugins.gif.get_gif(message))
    # Check for "I love you"
    match = re.search('i love you', message_text, re.IGNORECASE)
    if match:
      if message.sender['first'] == 'Catherine' and message.sender['last'] == 'Moresco':
        message.reply("I love you too, Mom!")
      else:
        message.reply("Uhh...thanks.")
    #check for OR
    match = re.search(r'\bOR\b', message_text)
    if match:
      terms = message_text.split('OR')
      if len(terms) < 2:
        return
      else:
        message.reply(terms[random.randrange(0, 2)])
    # Check for affirmation request
    match = re.search(r'right\, rachel\?', message_text, re.IGNORECASE)
    if match:
      message.reply("Right, " + message.sender['first'] + "!")

  # Message generation functions 
  def greet(self, addressee):
    return "Hello, " + addressee + "!"

