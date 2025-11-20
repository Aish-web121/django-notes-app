from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for(self, locator):
        """Wait until element is present."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_clickable(self, locator):
        """Wait until element is clickable."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        """Click an element, scrolling if needed."""
        element = self.wait_for_clickable(locator)
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            ActionChains(self.driver).move_to_element(element).click().perform()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator, text):
        """Type text into input field."""
        element = self.wait_for(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Return text of element."""
        return self.wait_for(locator).text

    def find_all(self, locator):
        """Return list of elements, safe if none found."""
        try:
            self.wait.until(lambda d: d.find_elements(*locator))
        except TimeoutException:
            return []
        return self.driver.find_elements(*locator)
