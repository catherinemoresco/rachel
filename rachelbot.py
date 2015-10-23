import requests, time, re, random, models.message

class RachelBot:
  def __init__(self, token):
    self.REQUEST_URL = 'https://api.telegram.org/' + token + '/'
    self.GIPHY_SEARCH_QUERY = 'http://api.giphy.com/v1/gifs/search?q='
    self.GIPHY_KEY = "&api_key=dc6zaTOxFJmzC"
    self.WOLFRAM_APP_ID = "UJ8389-HX5E7YYGVP"

    self.FILE_PATH = "gifs/"
    self.offset = 0

  def get_updates(self):
    try:
      r = requests.get(self.REQUEST_URL+ \
             'getUpdates?offset=' + str(self.offset))
    except:
      time.sleep(5)
      return

    for result in r.json()['result']:
      self.offset = result['update_id'] + 1
      try:
        self.process(result['message'])
      except:
        pass

  def process(self, message):
    message_text = message['text'].split('/Rachel')[-1]
    print "Processing message: '" + message_text + "'"
    # Check for greeting
    match = re.search(r'\b(hello|hey|hi)\b', message_text, re.IGNORECASE)
    if match:
      self.send_message(message['chat']['id'], 
                self.greet(message['from']['first_name']))
    # Check for a giphy search
    match = re.search('gif', message_text, re.IGNORECASE)
    if match:
      query_words = "+".join(message_text.split(" ")[1:])
      print query_words
      print "Getting photo..."
      gif = self.search_giphy(query_words)
      print "Sending photo..."
      self.send_photo(message['chat']['id'], gif)
    # Check for "I love you"
    match = re.search('i love you', message_text, re.IGNORECASE)
    if match:
      sender = message['from']
      if sender['first_name'] == 'Catherine' and sender['last_name'] == 'Moresco':
        self.send_message(message['chat']['id'], "I love you too, Mom!")
      else:
        self.send_message(message['chat']['id'], "Uhh...thanks.")
    #check for OR
    match = re.search('OR', message_text)
    if match:
      terms = message_text.split('OR')
      if len(terms) < 2:
        return
      else:
        self.send_message(message['chat']['id'], terms[random.randrange(0, 2)])
    # Check for affirmation request
    match = re.search(r'right\, rachel\?', message_text, re.IGNORECASE)
    if match:
      self.send_message(message['chat']['id'], "Right, " + message['from']['first_name'] + "!")

  def send_message(self, chat_id, string):
    r = requests.get(self.REQUEST_URL + \
      'sendMessage?chat_id=' + str(chat_id) + "&text=" + string + "&force_reply=True")

  def send_photo(self, chat_id, filename):
    r = requests.post(self.REQUEST_URL + \
      'sendDocument?chat_id=' + str(chat_id), files={'document': open(self.FILE_PATH + filename, 'rb')})
    print r.text

  # Message generation functions 
  def greet(self, addressee):
    return "Hello, " + addressee + "!"

  def search_giphy(self, query_words):
    r = requests.get(self.GIPHY_SEARCH_QUERY + query_words + self.GIPHY_KEY)
    print "Searching giphy..."
    results = r.json()['data']
    print "Got gif!"
    i = random.randrange(0, len(results))
    the_chosen_gif = results[i]['images']['original']['url']
    return self.get_file(the_chosen_gif)

  def get_file(self, url):
    filename = url.split('/')[-1] + '.gif'
    r = requests.get(url, stream=True)
    with open(self.FILE_PATH + filename, 'wb') as f:
      for chunk in r.iter_content(chunk_size=1024):
        if chunk:
          f.write(chunk)
          f.flush
    return filename