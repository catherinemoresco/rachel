import rachelbot, config

rachel = rachelbot.RachelBot(config.BOT_TOKEN)
while True:
    try:
        rachel.get_updates()
    except KeyboardInterrupt:
        print "Goodbye."
        break