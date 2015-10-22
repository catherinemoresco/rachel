import requests, time, re
import rachelbot

rachel = rachelbot.RachelBot()
while True:
    rachel.get_updates()