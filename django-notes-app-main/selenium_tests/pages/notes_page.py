from selenium.webdriver.common.by import By
from .base_page import BasePage

class NotesPage(BasePage):
    PAGE_HEADER_LOCATORS = [
        (By.TAG_NAME, "h1"),
        (By.CSS_SELECTOR, "h1.page-title"),
        (By.XPATH, "//h1[contains(., 'My Notes') or contains(., 'Notes')]"),
    ]

    ADD_BUTTON_LOCATORS = [
        (By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add')]"),
        (By.XPATH, "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add')]"),
        (By.CSS_SELECTOR, "button.btn-add, button.add-note, a.btn-add"),
    ]

    NOTE_ITEMS_LOCATORS = [
        (By.CSS_SELECTOR, ".note-item"),
        (By.CSS_SELECTOR, ".note"),
        (By.CSS_SELECTOR, "li.note"),
        (By.XPATH, "//div[contains(@class,'note')]"),
    ]

    def _first_header_text(self):
        for loc in self.PAGE_HEADER_LOCATORS:
            try:
                return self.get_text(loc)
            except Exception:
                continue
        return ""

    def verify_loaded(self):
        """Return page header or page title."""
        header = self._first_header_text()
        if header:
            return header
        return self.driver.title or ""

    def click_add_button(self):
        """Click the first Add button found."""
        for loc in self.ADD_BUTTON_LOCATORS:
            try:
                self.click(loc)
                return
            except Exception:
                continue
        raise Exception("Add button not found or not clickable.")

    def get_notes_count(self):
        """Return number of notes on the page."""
        for loc in self.NOTE_ITEMS_LOCATORS:
            elems = self.find_all(loc)
            if elems:
                return len(elems)
        return 0
