class RachelMessage
	def init(self, message_json):
		self.text = message_json.text
		self.chat_id = message_json['chat']['id']
		self.sender = {first: message_json['from']['first_name'],
					   last: message_json['from']}

