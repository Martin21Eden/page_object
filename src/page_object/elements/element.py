from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from page_object.locator_generator import LocatorGenerator
from page_object.expected_conditions.element_exists import element_exists
from page_object.expected_conditions.element_has_value import element_has_value


class Element(LocatorGenerator, object):
    """
    Base class to represent HTML Elements
    """

    def __init__(self, element):
        """
        Arg:
            element (selenium.webdriver.webelement)
        """
        self._load_locator(element)
        self.generate_locators()
        self.element = element

    def text(self):
        """
        Getter for text within the element
        """
        return self.element.text

    def clear(self):
        """
        Clears the text if its a text entry element.
        """
        return self.element.clear()

    def click(self):
        """
        Clicks the element.
        """
        return self.element.click()

    def hover(self):
        """
        Hovers over an element.
        """
        # The react-bootstrap overlay trigger doesn't register the move_to_element unless there's
        # another mouse action ahead of time.
        ActionChains(self.element.parent).move_by_offset(10, 10).move_to_element(self.element).perform()

    def class_name(self):
        """
        Gets the given attribute or property of the element.

        Return:
            The class for the element
        """
        return self.attribute('class')

    def attribute(self, attribute):
        """
        Gets the given attribute or property of the element.

        Args:
            attribute: name of attribute (e.g. class)
        """
        return self.element.get_attribute(attribute)

    def when_present(self, timeout=5):
        """
        Waits for element to be present on the current page.

        Args:
            timeout (integer): seconds to wait before throwing exception.
        """
        self.wait_unitl(element_exists(self.element))

    def has_text(self, text, timeout=5):
        def comparator(actual):
            return text in actual

        self.wait_unitl(element_has_value(self.text, comparator), timeout)

    def is_not_empty(self, timeout=5):
        def comparator(current_value):
            return current_value is not None or current_value is not ''

        self.wait_unitl(element_has_value(self.text, comparator), timeout)

    def wait_unitl(self, condtion, timeout=5):
        wait = WebDriverWait(self.element, timeout)
        wait.until(condtion)

    def send_keys(self, keys):
        """
        Simulates key entry into the element.
        """
        return self.element.send_keys(keys)

    def _load_locator(self, element):
        from page_object.locator import Locator
        self.locator = Locator(element)