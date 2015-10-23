import rachelbot, config

rachel = rachelbot.RachelBot(config.BOT_TOKEN)
print "Hello!"
while True:
    try:
        rachel.get_updates()
    except KeyboardInterrupt:
        print "Goodbye."
        break