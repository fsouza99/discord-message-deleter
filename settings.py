import json
from os import listdir

CONFIG_FILE = "config\\config.json"
CONFIG_TEMPLATE = "config\\config-template.json"

class Settings():

	def load_config(self):
		with open(CONFIG_FILE, encoding='utf8') as file:
			data = json.load(file)
		for scope in data.keys():
			for key, value in data[scope].items():
				value = "" if value is None else value
				setattr(self, key, value)
		return

	def search_key(self) -> str:
		if self.searchkey:
			return self.searchkey
		return \
			  f"de: {self.username} " \
			+ f"em: {self.channel} " \
			+ f"tem: {self.item} " \
			+ f"menciona: {self.mention} " \
			+ f"antes: {self.before} " \
			+ f"depois: {self.after} " \
			+ f"durante: {self.during} " \
			+ f"{self.sentence}"

	def briefing(self) -> str:
		return f"User: {self.username}\nTarget server: {self.server}\nSearch key: \u0022{self.search_key()}\u0022"





