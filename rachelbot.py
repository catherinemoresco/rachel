import requests, time, re, random, config
from  models.message import RachelMessage

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
      query_words = "+".join(message_text.split(" ")[1:])
      print query_words
      print "Getting photo..."
      gif = self.search_giphy(query_words)
      print "Sending photo..."
      self.send_photo(message.chat_id, gif)
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

  def send_photo(self, chat_id, filename):
    r = requests.post(config.REQUEST_URL + \
      'sendDocument?chat_id=' + str(chat_id), files={'document': open(config.FILE_PATH + filename, 'rb')})
    print r.text

  # Message generation functions 
  def greet(self, addressee):
    return "Hello, " + addressee + "!"

  def search_giphy(self, query_words):
    r = requests.get(config.GIPHY_SEARCH_QUERY + query_words + config.GIPHY_KEY)
    print "Searching giphy..."
    results = r.json()['data']
    print "Got gif!"
    i = random.randrange(0, len(results))
    the_chosen_gif = results[i]['images']['original']['url']
    return self.get_file(the_chosen_gif)

  def get_file(self, url):
    filename = url.split('/')[-1] + '.gif'
    r = requests.get(url, stream=True)
    with open(config.FILE_PATH + filename, 'wb') as f:
      for chunk in r.iter_content(chunk_size=1024):
        if chunk:
          f.write(chunk)
          f.flush
    return filename