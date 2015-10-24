import requests, time, re, random, config
from models.message import RachelMessage
import plugins.gif

class RachelBot:
  def __init__(self, token):
    self.offset = 0

  def get_updates(self):
    """
    Make a request for updates to Telegram and process result.
    """
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
    """
    The main dispatch function.
    Takes in a message, determines appropriate response, and sends a reply.
    """
    if not message.text:
      return
    message_text = message.text.split('/Rachel')[-1]
    print "Processing message: '" + message_text + "'"

    # Check for greeting
    match = re.search(r'\b(hello|hey|hi)\b', message_text, re.IGNORECASE)
    if match:
      message.reply(self.greet(message.sender['first']))

    # Check for "I love you"
    match = re.search('i love you', message_text, re.IGNORECASE)
    if match:
      message.reply(self.love(message.sender))

    #check for OR
    match = re.search(r'\bOR\b', message_text)
    if match:
      message.reply(self.choose(message_text))

    # Check for affirmation request
    match = re.search(r'right\, rachel\?', message_text, re.IGNORECASE)
    if match:
      message.reply(self.affirm(message.sender))

    # Check for a giphy search
    match = re.search('gif', message_text, re.IGNORECASE)
    if match:
      message.reply_with_photo(plugins.gif.get_gif(message))

  # Message generation functions 

  def greet(self, addressee):
    return "Hello, " + addressee + "!"

  def love(self, sender):
      if sender['first'] == 'Catherine' and sender['last'] == 'Moresco':
        return "I love you too, Mom!"
      else:
        return "Uhh...thanks."

  def choose(self, message_text):
    terms = message_text.split('OR')
    if len(terms) < 2:
      return
    else:
      return terms[random.randrange(0, 2)]   

  def affirm(self, sender):
      return "Right, " + sender['first'] + "!"

