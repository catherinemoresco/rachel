"""
gif.py
a plugin module to encapsulate calls to the Giphy API
"""

import requests, config, random, re

def get_gif(message):
  """ Search for a gif using query words
      ::return: file name of saved gif
  """
  query_words = "+".join((re.sub('gif', '', message.text, count=1)).split(" "))
  return search_giphy(query_words)

def search_giphy(query_words):
  """ Given a list of query words, make a request to the Giphy API """
  r = requests.get(config.GIPHY_SEARCH_QUERY + query_words + config.GIPHY_KEY)
  results = r.json()['data']
  if len(results):
    i = random.randrange(0, len(results))
    the_chosen_gif = results[i]['images']['original']['url']
    return get_file(the_chosen_gif)
  return None

def get_file(url):
  """ Download fime from link and save"""
  filename = 'gif_from_Rachel.gif'
  r = requests.get(url, stream=True)
  with open(config.FILE_PATH + filename, 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024):
      if chunk:
        f.write(chunk)
        f.flush
  return filename