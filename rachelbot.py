import requests, time, re, random

class RachelBot:
  def __init__(self):
    self.REQUEST_URL = 'https://api.telegram.org/***REDACTED***/'
    self.GIPHY_SEARCH_QUERY = 'http://api.giphy.com/v1/gifs/search?q='
    self.GIPHY_KEY = "&api_key=dc6zaTOxFJmzC" # the public beta token
    self.FILE_PATH = "gifs/"
    self.offset = 0

  def get_updates(self):
    r = requests.get(self.REQUEST_URL+ \
             'getUpdates?offset=' + str(self.offset))
    for result in r.json()['result']:
      self.offset = result['update_id'] + 1
      try:
        self.process(result['message'])
      except:
        pass

  def process(self, message):
    # Check for greeting
    match = re.search('(hello|hey|hi)', message['text'], re.IGNORECASE)
    if match:
      self.send_message(message['chat']['id'], 
                self.greet(message['from']['first_name']))
    # Check for a giphy search
    match = re.search('gif', message['text'], re.IGNORECASE)
    if match:
      query_words = "+".join(message['text'].split(" ")[2:])
      print query_words
      print "getting photo..."
      gif = self.search_giphy(query_words)
      print "sending photo..."
      self.send_photo(message['chat']['id'], gif)

  def send_message(self, chat_id, string):
    r = requests.get(self.REQUEST_URL + \
      'sendMessage?chat_id=' + str(chat_id) + "&text=" + string)

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
    i = random.randrange(0, len(results))
    the_chosen_gif = results[i]['images']['original']['url']
    return self.get_file(the_chosen_gif)

  def get_file(self, url):
    filename = url.split('/')[-2] + '.gif'
    r = requests.get(url, stream=True)
    with open(self.FILE_PATH + filename, 'wb') as f:
      for chunk in r.iter_content(chunk_size=1024):
        if chunk:
          f.write(chunk)
          f.flush
    return filename
