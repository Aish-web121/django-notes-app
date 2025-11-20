# selenium_tests/pages/noteformpage.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import time
from .base_page import BasePage

class NoteFormPage(BasePage):
    """
    Robust Note form page object.
    Tries many locator strategies; falls back to the first visible text input/textarea.
    Saves debug artifacts if title/body elements cannot be found.
    """

    # common title input candidates
    TITLE_LOCATORS = [
        (By.NAME, "title"),
        (By.ID, "title"),
        (By.ID, "id_title"),
        (By.CSS_SELECTOR, "input[name='title']"),
        (By.CSS_SELECTOR, "input[placeholder*='title']"),
        (By.CSS_SELECTOR, "input[aria-label*='title']"),
        (By.CSS_SELECTOR, "input[type='text']"),
        (By.XPATH, "//label[contains(., 'Title')]/following::input[1]"),
    ]

    BODY_LOCATORS = [
        (By.NAME, "body"),
        (By.ID, "body"),
        (By.ID, "id_body"),
        (By.CSS_SELECTOR, "textarea[name='body']"),
        (By.CSS_SELECTOR, "textarea[placeholder*='body']"),
        (By.CSS_SELECTOR, "textarea[aria-label*='body']"),
        (By.CSS_SELECTOR, "textarea"),
        (By.XPATH, "//label[contains(., 'Body')]/following::textarea[1]"),
    ]

    SAVE_LOCATORS = [
        (By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'save')]"),
        (By.XPATH, "//button[contains(., 'Create') or contains(., 'Add') or contains(., 'Submit')]"),
        (By.CSS_SELECTOR, "button[type='submit']"),
    ]

    def _try_locators(self, candidate_list):
        """Return the first element found for given locators, or None."""
        for loc in candidate_list:
            try:
                el = self.driver.find_element(*loc)
                # ensure it's visible and enabled
                if el.is_displayed() and el.is_enabled():
                    return el
            except Exception:
                continue
        return None

    def _fallback_first_text_input(self):
        """Fallback: return the first visible text input or textarea on the page."""
        # check inputs
        inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input:not([type]) , textarea")
        for el in inputs:
            try:
                if el.is_displayed() and el.is_enabled():
                    return el
            except Exception:
                continue
        return None

    def _get_field(self, candidate_list, field_name):
        """Find a field using locators with fallback and save debug artifacts if not found."""
        el = self._try_locators(candidate_list)
        if el:
            return el

        # fallback to first text input / textarea
        el = self._fallback_first_text_input()
        if el:
            return el

        # debug: save artifacts so user can inspect
        try:
            self.save_debug_artifacts("noteformpage")
        except Exception:
            pass

        raise Exception(f"{field_name} input not found. Saved debug artifacts (noteformpage_*).")

    def fill_title(self, title):
        el = self._get_field(self.TITLE_LOCATORS, "Title")
        try:
            el.clear()
        except Exception:
            pass
        el.click()
        el.send_keys(title)

    def fill_body(self, body):
        el = self._get_field(self.BODY_LOCATORS, "Body")
        try:
            el.clear()
        except Exception:
            pass
        el.click()
        el.send_keys(body)

    def save(self):
        # try save locators
        for loc in self.SAVE_LOCATORS:
            try:
                el = self.driver.find_element(*loc)
                if el.is_displayed() and el.is_enabled():
                    el.click()
                    return
            except Exception:
                continue

        # fallback: try submit on a form element if present
        try:
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            for f in forms:
                try:
                    if f.is_displayed():
                        f.submit()
                        return
                except Exception:
                    continue
        except Exception:
            pass

        # if still not found, save debug artifacts and raise
        try:
            self.save_debug_artifacts("noteformpage_save")
        except Exception:
            pass
        raise Exception("Save button not found. Saved debug artifacts (noteformpage_*).")
