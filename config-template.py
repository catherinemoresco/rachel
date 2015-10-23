""" config-template.py
    a template for your RachelBot config file 
"""

# REQUIRED VALUES ======================================================
# your bot will not run without these
FILE_PATH =  ''

BOT_TOKEN = ''
REQUEST_URL = 'https://api.telegram.org/' + BOT_TOKEN + '/'


# PLUGIN-SPECIFIC VALUES ===============================================
#giphy:
GIPHY_SEARCH_QUERY = 'http://api.giphy.com/v1/gifs/search?q='
GIPHY_KEY = "&api_key=dc6zaTOxFJmzC" # This is a public beta key, subject to rate-limiting

#wolfram:
WOLFRAM_APP_ID = ''