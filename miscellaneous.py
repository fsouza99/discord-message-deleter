from settings import *

def search_key():
	if SEARCHKEY is None:
		return \
		  f"de: {USERNAME} " \
		+ f"em: {CHANNEL} " \
		+ f"tem: {ITEM} " \
		+ f"menciona: {MENTION} " \
		+ f"antes: {BEFORE} " \
		+ f"depois: {AFTER} " \
		+ f"durante: {DURING} " \
		+ f"{SENTENCE}"
	return SEARCHKEY

def formatted_time(seconds: int):
	h, r = divmod(seconds, 3600)
	m, s = divmod(r, 60)
	return f"{h:02}:{m:02}:{s:02}"


