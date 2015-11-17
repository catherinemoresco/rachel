import datetime, dateutil.parser

def store_reminder(state_dict, message):
  # try:
    activity_date = dateutil.parser.parse(message.text, fuzzy=True)
    if activity_date < datetime.datetime.now():
      return "That date has already passed!"
    # strip initial "remind me"
    activity = message.text.split("remind me")[-1]
    chat_reminders = state_dict["event_reminders"].get(message.chat_id)
    if chat_reminders == None:
      chat_reminders = state_dict["event_reminders"][message.chat_id] = []
    chat_reminders.append((str(activity_date), activity))
    print state_dict
    return "Got it!"
  # except:
  #   return "Sorry, can't handle that right now."

