import time

from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains

class Bot():

	def __init__(self, driver, settings):
		self.driver = driver
		self.settings = settings

	def get_element(self, locator, origin=None):
		"""
		Returns the pointed element or None if it does not exist.
		"""
		if origin is None:
			origin = self.driver
		try:
			element = origin.find_element(locator[0], locator[1])
		except Exception:
			return None
		return element

	def get_elements(self, locator, origin=None):
		"""
		Returns the pointed elements or None if they do not exist.
		"""
		if origin is None:
			origin = self.driver
		try:
			elements = origin.find_elements(locator[0], locator[1])
		except Exception:
			return None
		return elements

	# Simple interactions

	def right_click(self, element):
		return ActionChains(self.driver).context_click(element).perform()

	def scroll_to(self, element):
		return ActionChains(self.driver).scroll_to_element(element).perform()

	def type(self, text: str):
		return ActionChains(self.driver).send_keys(text).perform()

	def press_enter(self):
		return ActionChains(self.driver).send_keys(Keys.ENTER).perform()

	def type_and_confirm(self, message: str):
		self.type(message)
		time.sleep(0.2) # Safety measure.
		self.press_enter()
		return

	def shift_click(self, target):
		"""
		Click somewhere while holding SHIFT.
		"""
		ActionChains(self.driver).key_down(Keys.SHIFT).perform()
		time.sleep(0.1) # Safety measure.
		ActionChains(self.driver).click(target).perform()
		time.sleep(0.1) # Safety measure.
		ActionChains(self.driver).key_up(Keys.SHIFT).perform()
		return

	def refresh_page(self):
		return self.driver.refresh()

	# Complex interactions

	def perform_login(self):
		"""
		Current URL: https://discord.com/login (login page)
		This method performs login.
		"""
		form = self.driver.find_element(By.TAG_NAME, 'form')

		email_input = form.find_element(By.NAME, 'email')
		email_input.clear()
		email_input.send_keys(self.settings.email)

		password_input = form.find_element(By.NAME, 'password')
		password_input.clear()
		password_input.send_keys(self.settings.password)

		login_button = form.find_elements(By.TAG_NAME, "button")[1]
		login_button.click()

		return

	def select_server(self):
		"""
		Current URL: https://discord.com/channels/@me ("lobby" page)
		Enters the target server.
		"""
		clickable_div = self.get_element(
			locator=(By.CSS_SELECTOR, f"[data-dnd-name=\u0022{self.settings.server}\u0022]"))
		clickable_div.click()
		return

	def search_messages(self):
		"""
		Current URL: https://discord.com/channels/<digits>/<digits> (inside server).
		Handles the search box to find the messages that match the user's parameters.
		"""
		clear_search_button = self.driver.find_element(
			By.CSS_SELECTOR, f"[aria-label=\u0022Limpar busca\u0022]")
		clear_search_button.click()

		search_box = self.driver.find_element(
			By.CSS_SELECTOR, f"[aria-label=\u0022Buscar\u0022]")
		search_box.click()
		
		self.type_and_confirm(self.settings.search_key())

		time_filter_button = self.driver.find_element(
			By.XPATH, "//div[text()='Antigo']")
		time.sleep(1) # Safety measure.
		time_filter_button.click()
		time.sleep(1) # Safety measure.

		return

	def delete_searched_msgs(self, target_count) -> int:
		"""
		Current URL: https://discord.com/channels/<digits>/<digits> (inside server).
		Delete a number of search-resulting messages while respecting wait intervals to avoid skipping.
		Returns the number of deleted messages.
		"""
		progress = 0
		parent_div = self.get_element(
			locator=(By.CSS_SELECTOR, 'div#search-results'))

		while True:

			print('Loading new results.')

			if parent_div is None:
				print("New search results could not be retrieved.")
				break

			item_groups = self.get_elements(
				origin=parent_div,
				locator=(By.TAG_NAME, 'ul'))
			if item_groups is None:
				print('Messages could not be retrieved from search results.')
				break

			for group in item_groups:

				if progress >= target_count:
					break

				items = group.find_elements(By.TAG_NAME, 'li')
				for item in items[:target_count - progress]:
					self.scroll_to(item)
					self.right_click(item)
					delete_button = self.get_element(
						locator=(By.CSS_SELECTOR, 'div#message-delete'))
					time.sleep(0.2) # Safety measure.
					self.shift_click(delete_button)
					progress += 1
					print(f'\rDeleted msgs: {progress}', end='')
			print()

			if progress >= target_count:
				print("Target count reached.")
				break

			next_page_button = self.get_element(
				locator=(By.XPATH, "//button[@rel=\u0022next\u0022]"))
			if next_page_button is None:
				print('No \u0022Next page\u0022 button found.')
				break
			if not next_page_button.is_enabled():
				print('No more apparent result pages.')
				break
			next_page_button.click()
			
			parent_div = self.get_element(
				locator=(By.CSS_SELECTOR, 'div#search-results'))
		
		return progress

	def search_and_delete(self, target_count) -> int:
		"""
		Current URL: https://discord.com/channels/<digits>/<digits> (inside server).
		Performs a search and delete all resulting messages.
		"""
		print('Searching for messages.')
		self.search_messages()
		print('Deleting search results.')
		deletions = self.delete_searched_msgs(target_count)
		return deletions