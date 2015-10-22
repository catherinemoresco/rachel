import requests, time, re
import rachelbot

rachel = rachelbot.RachelBot()
while True:
    try:
        rachel.get_updates()
    except KeyboardInterrupt:
        print "Goodbye."
        break