import time

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from settings import Settings


class Bot:

    def __init__(self, driver: WebDriver, settings: Settings):
        self.driver = driver
        self.settings = settings

    def try_find_element(
        self, by: By, value: str, src: WebElement | None = None):
        """Return the referred element or None if it does not exist.

        This method wraps the namesake Selenium method to avoid exceptions
        being raised when the referred element can't be found.
        """
        if src is None:
            src = self.driver
        try:
            element = src.find_element(by, value)
        except Exception:
            return None
        return element

    def refresh_page(self):
        return self.driver.refresh()

    # Simple interactions.

    def right_click(self, element: WebElement):
        return ActionChains(self.driver).context_click(element).perform()

    def scroll_to(self, element: WebElement):
        return ActionChains(self.driver).scroll_to_element(element).perform()

    def type(self, text: str):
        return ActionChains(self.driver).send_keys(text).perform()

    def press_enter(self):
        return ActionChains(self.driver).send_keys(Keys.ENTER).perform()

    # Chained simple interactions.

    def type_and_confirm(self, message: str):
        """Type string and press ENTER."""
        self.type(message)
        time.sleep(.2)
        self.press_enter()
        return

    def shift_click(self, element: WebElement):
        """Click on element while holding SHIFT."""
        ActionChains(self.driver).key_down(Keys.SHIFT).perform()
        time.sleep(.1)
        ActionChains(self.driver).click(element).perform()
        time.sleep(.1)
        ActionChains(self.driver).key_up(Keys.SHIFT).perform()
        return

    # Complex interactions.

    def perform_login(self):
        """Perform login.

        Current URL (login page): https://discord.com/login
        """
        form = self.driver.find_element(By.TAG_NAME, 'form')

        email_input = form.find_element(By.NAME, 'email')
        email_input.clear()
        email_input.send_keys(self.settings.email)

        password_input = form.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(self.settings.password)

        login_btn = form.find_elements(By.TAG_NAME, 'button')[1]
        login_btn.click()

        return

    def select_server(self):
        """Enter the target server.

        Current URL ("lobby" page): https://discord.com/channels/@me
        """
        self.driver.find_element(
            By.CSS_SELECTOR,
            f'[data-dnd-name="{self.settings.server}"]'
            ).click()
        return

    def search_messages(self):
        """Handle the search box to find target messages.

        Current URL (server page): https://discord.com/channels/<num>/<num>
        """
        # Clear search box if not empty.
        clear_search_icon = self.try_find_element(
            By.CSS_SELECTOR, f'svg[aria-label="Limpar"]')
        if clear_search_icon is not None:
            clear_search_icon.find_element(By.XPATH, 'ancestor::div').click()
            time.sleep(.2)
        
        # Click on search box.
        self.driver.find_element(
            By.CSS_SELECTOR, f'div[aria-label="Buscar"]').click()
        time.sleep(.2)

        # Enter search key.
        self.type_and_confirm(self.settings.search_key())
        time.sleep(.2)

        # Open sorting options menu.
        self.driver.find_element(
            By.CSS_SELECTOR, f'button[aria-label="Ordenar"]').click()
        time.sleep(.2)

        # Sort by time, with oldest on top.
        self.driver.find_element(
            By.XPATH, '//div[text()="Mais antigos"]'
            ).find_element(By.XPATH, 'ancestor::div'
            ).click()
        time.sleep(.2)

        return

    def delete_searched_msgs(self) -> int:
        """Delete search-resulting messages respecting predefined limit.

        Current URL (server page): https://discord.com/channels/<num>/<num>
        """
        if self.try_find_element(By.ID, 'search-results') is None:
            print('No search results.')
            return

        while True:
            items = self.driver.find_elements(
                By.CSS_SELECTOR, 'li[id^="search-results-"]')

            for item in items:
                self.scroll_to(item)

                self.right_click(item)
                time.sleep(.3)

                self.shift_click(
                    self.driver.find_element(By.ID, 'message-delete'))

                self.progress += 1
                print(f'\rDeleted msgs: {self.progress}', end='')

                if self.progress >= self.target_count:
                    print('\nTarget count reached.')
                    return
            print()

            next_page_btn = self.try_find_element(
                By.CSS_SELECTOR, 'button[rel="next"]')
            if next_page_btn is None:
                print('No "Next page" button found.')
                break
            if not next_page_btn.is_enabled():
                print('No more apparent result pages.')
                break
            next_page_btn.click()
            time.sleep(1)
            print('Next result page.')

        return

    def search_and_delete(self, target_count: int) -> int:
        """Perform a search and delete a number of resulting messages.

        Current URL (server page): https://discord.com/channels/<num>/<num>
        """
        self.progress = 0
        self.target_count = target_count

        print('Searching for messages.')
        self.search_messages()

        print('Deleting search results.')
        self.delete_searched_msgs()

        return self.progress

