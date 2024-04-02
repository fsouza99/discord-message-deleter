import time

from miscellaneous import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver import Keys, ActionChains

class Bot():

	def __init__(self, driver):
		self.driver = driver

	def get_element(self, locator):
		"""
		Returns the element or None if it does not exist.
		"""
		try:
			element = self.driver.find_element(locator[0], locator[1])
		except Exception:
			return None
		return element

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
		time.sleep(0.2)
		self.press_enter()
		return

	def shift_click(self, target):
		"""
		Click somewhere while holding SHIFT.
		"""
		ActionChains(self.driver).key_down(Keys.SHIFT).perform()
		time.sleep(0.1)
		ActionChains(self.driver).click(target).perform()
		time.sleep(0.1)
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
		email_input.send_keys(EMAIL)

		password_input = form.find_element(By.NAME, 'password')
		password_input.clear()
		password_input.send_keys(PASSWORD)

		login_button = form.find_elements(By.TAG_NAME, "button")[1]
		login_button.click()

		return

	def select_server(self):
		"""
		Current URL: https://discord.com/channels/@me ("lobby" page)
		Enters the target server.
		"""
		clickable_div = self.get_element(locator=(
			By.CSS_SELECTOR, f"[data-dnd-name=\u0022{SERVER}\u0022]"))
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
		
		self.type_and_confirm(search_key())
		time.sleep(1.5)
		
		time_filter_button = self.driver.find_element(
			By.XPATH, "//div[text()='Antigo']")
		time_filter_button.click()
		
		time.sleep(1.5)
		return

	def delete_searched_msgs(self) -> int:
		"""
		Current URL: https://discord.com/channels/<digits>/<digits> (inside server).
		Delete all search-resulting messages.
		Returns the number of deleted messages.
		"""
		progress = 0
		parent_div = self.get_element(
			locator=(By.CSS_SELECTOR, 'div#search-results'))
		if parent_div is None:
			print("No messages could be retrieved.")
			return progress

		while True:

			print('New page.')
			items = parent_div.find_element(By.TAG_NAME, 'ul').find_elements(
				By.TAG_NAME, 'li')

			for item in items:
				self.scroll_to(item)
				self.right_click(item)
				time.sleep(0.25)
				delete_button = self.get_element(locator=(
					By.CSS_SELECTOR, 'div#message-delete'))
				self.shift_click(delete_button)
				time.sleep(0.25)
				progress += 1
				print(f'\rDeleted msgs: {progress}', end='')
			print()

			next_page_button = self.get_element(locator=(
				By.XPATH, "//button[@rel=\u0022next\u0022]"))
			if next_page_button is None:
				print('No \u0022Next page\u0022 button found.')
				return progress
			if not next_page_button.is_enabled():
				print('No more apparent pages.')
				return progress
			next_page_button.click()
			time.sleep(1)
			parent_div = self.get_element(locator=(
				By.CSS_SELECTOR, 'div#search-results'))
		
		return progress

	def search_and_delete(self) -> int:
		"""
		Current URL: https://discord.com/channels/<digits>/<digits> (inside server).
		Performs a search and delete all resulting messages.
		"""
		print('Searching for messages.')
		self.search_messages()
		print('Deleting search results.')
		return self.delete_searched_msgs()