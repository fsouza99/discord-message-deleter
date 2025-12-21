import time

from selenium import webdriver

from interaction import Bot
from miscellaneous import formatted_time, set_environment
from settings import Settings


if set_environment():
    print('Enter your input in "config\\config.json" before running again.')
    exit(0)

settings = Settings()
print(settings.briefing())

print('Setting driver options.')
options = webdriver.ChromeOptions()
options.add_argument('-headless')
options.add_argument('--log-level=3')

# Chrome specific.
service = webdriver.ChromeService(log_output='chrome-driver.log')

print('Loading web driver.')
driver = webdriver.Chrome(options=options, service=service)
driver.implicitly_wait(10)

print('\nSetting bot.')
bot = Bot(driver, settings)

print('Loading login page.')
driver.get("https://discord.com/login")

# Auto login.
h = 1
while True:
    print(f'Login attempt ({h}/{settings.login_attempts}): ', end='')

    try:
        bot.perform_login()
        print('Success.')
        break
    except Exception as e:
        print('Failure.')

    h += 1
    if h > settings.login_attempts:
        print('Login could not be performed.')
        exit(1)

    print('Refreshing login page.')
    driver.refresh()

# Target server selection.
h = 1
while True:
    print(
        'Server selection attempt ',
        f'({h}/{settings.selection_attempts}): ',
        end='')

    try:
        bot.select_server()
        print('Success.')   
        break
    except Exception as e:
        print('Failure.')

    h += 1
    if h > settings.selection_attempts:
        print('Target server could not be selected.')
        exit(1)

    print('Refreshing channels page.')
    driver.refresh()

# Timer initialization.
print('Starting timer.')
start_time = time.time()

# Search and deletion of messages.
nil_count = progress = 0
while (
    nil_count <= settings.nil_tolerance
    and progress < settings.target_count):

    print(f'\nNew iteration of search and delete.')
    driver.refresh()

    try:
        # Inform the bot with the right number of messages to delete.
        status = bot.search_and_delete(settings.target_count - progress)
    except Exception as e:
        print('\nUnexpected error:', e)
        break

    if status == 0:
        # Total iterations with zero messages deleted.
        nil_count += 1
    else:
        # Total messages deleted.
        progress += status

    elapsed_time = time.time() - start_time
    print(f'\nTotal progress: {progress}')
    print(f'Zero status occurences: {nil_count}')
    print(f'Elapsed time: {formatted_time(int(elapsed_time))}')

# Finishing session.

print('\nInteraction finished.\nClosing the driver.')
driver.quit()

