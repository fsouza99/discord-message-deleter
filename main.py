"""
Define execution parameters on settings.py before running this script.
"""

import importlib
import time

import interactor

from miscellaneous import *

from selenium import webdriver

print('Setting driver options.')
options = webdriver.ChromeOptions()
options.add_argument('-headless')
options.add_argument('--log-level=3')

# Chrome specific.
service = webdriver.ChromeService(log_output='chrome-log')

print('Loading web driver.')
driver = webdriver.Chrome(options=options, service=service)
driver.implicitly_wait(10)

print('Setting bot.')
bot = interactor.Bot(driver)

print('Loading login page.')
driver.get("https://discord.com/login")

# Auto login.

h = 1
while h <= LOGIN_ATTEMPTS:
	try:
		print(f'Login attempt ({h}/{LOGIN_ATTEMPTS}): ', end='')
		bot.perform_login()
		print('Success.')
		break
	except Exception as e:
		print('Failure.')
	print('Refreshing login page.')
	driver.refresh()
	h += 1

if h > LOGIN_ATTEMPTS:
	print('Login could not be performed.')
	exit(1)

# Target server selection.

h = 1
while h <= SELECTION_ATTEMPTS:
	try:
		print(f'Server selection attempt ({h}/{SELECTION_ATTEMPTS}): ', end='')
		bot.select_server()
		print('Success.')	
		break
	except Exception as e:
		print('Failure.')
	print('Refreshing channels page.')
	driver.refresh()
	h += 1

if h > SELECTION_ATTEMPTS:
	print('Target server could not be selected.')
	exit(1)

# Initializing timer.

print('Starting timer.')
start_time = time.time()

# Search and deletion of messages.

nil_count, progress = 0, 0
while nil_count <= NIL_TOLERANCE and progress < TARGET_COUNT:
	try:
		print(f'\nNew iteration of search and delete.')
		status = bot.search_and_delete()
	except Exception as e:
		print('\nERROR.', end='')
		status = 0
	progress += status
	elapsed_time = time.time() - start_time
	print(f'\nIteration interrupted.\nElapsed time: {formatted_time(int(elapsed_time))}.')
	if status == 0:
		nil_count += 1

# Finishing session.

print('\nInteraction finished.\nClosing the driver.')
driver.quit()




