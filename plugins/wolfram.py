"""
  wolfram.py 
  a plugin to handle queries to wolfram alpha
"""

import config, requests, re
from xml.etree import ElementTree

def get_answer(message):
  """
  make a request to the wolfram alpha API and return result
  """
  # All messages will lead with "rachel," and end with "?". 
  # We strip both of these before making the request.
  question = re.sub('(rachel,|Rachel,)', '',message.text, re.IGNORECASE)[:-1]
  r = requests.get(config.WOLFRAM_QUERY_URL + question)
  root = ElementTree.fromstring(r.content)
  for pod in root.findall('pod'):
    if pod.get('title') == "Result" or \
    pod.get('title') == "Definitions" or \
    pod.get('title') == "Decimal approximation":
      for subpod in pod.find('subpod'):
        if subpod.get('title') == None:
          return subpod.text
  return "What do I look like, Google? \n " + config.GOOGLE_SEARCH_LINK + question

