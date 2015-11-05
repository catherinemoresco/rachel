import requests, time, re, random, config
from models.message import RachelMessage
import plugins.gif, plugins.wolfram

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

    try:
      for result in r.json()['result']:
        if result['message']:
            message = RachelMessage(result['message'])
            self.process(message)
    except:
      pass

    self.offset += 1


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
    if re.search(r'\b(hello|hey|hi)\b', message_text, re.IGNORECASE):
      message.reply(self.greet(message.sender['first']))

    # Check for "I love you"
    if re.search('i love you', message_text, re.IGNORECASE):
      message.reply(self.love(message.sender))

    #check for OR
    if re.search(r'\bOR\b', message_text):
      message.reply(self.choose(message_text))

    # Check for affirmation request
    if re.search(r'right\, rachel\?', message_text, re.IGNORECASE):
      message.reply(self.affirm(message.sender))

    # Check for a giphy search
    if re.search('gif', message_text, re.IGNORECASE):
      message.reply_with_photo(plugins.gif.get_gif(message))

    # Check for a general-knowledge question
    if re.search(r'^(rachel\,).*\?$', message_text, re.IGNORECASE):
      message.reply(plugins.wolfram.get_answer(message))


  # Built-in me\ssage generation functions 
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

