import requests, config, random, re

def get_gif(message):
  query_words = "+".join((re.sub('gif', '', message.text, count=1)).split(" "))
  return search_giphy(query_words)

def search_giphy(query_words):
  r = requests.get(config.GIPHY_SEARCH_QUERY + query_words + config.GIPHY_KEY)
  results = r.json()['data']
  i = random.randrange(0, len(results))
  the_chosen_gif = results[i]['images']['original']['url']
  return get_file(the_chosen_gif)

def get_file(url):
  filename = 'gif_from_Rachel.gif'
  r = requests.get(url, stream=True)
  with open(config.FILE_PATH + filename, 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024):
      if chunk:
        f.write(chunk)
        f.flush
  return filename