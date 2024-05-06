import json

from os import listdir

from settings import CONFIG_TEMPLATE, CONFIG_FILE

def set_environment() -> bool:
	"""
	Create a configuration file if it does not exist already.
	The template pointed by CONFIG_TEMPLATE is used as reference.
	"""
	if "config.json" in listdir("config"):
		return False
	with open(CONFIG_TEMPLATE, encoding='utf8') as file:
		data = json.load(file)
	with open(CONFIG_FILE, 'w', encoding='utf8') as file:
		json.dump(data, file, indent=4)
	return True

def formatted_time(seconds: int) -> str:
	h, r = divmod(seconds, 3600)
	m, s = divmod(r, 60)
	return f"{h:02}:{m:02}:{s:02}"

