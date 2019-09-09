import os
import time

from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from framework.ui.webelement_wrapper import WebElement_Wrapper


class SeleniumLibraries(object):

    def __init__(self, browser=None, base_url=None):
        self.browser = browser
        self.base_url = base_url
        self.default_wait_time = 30

    def find_element(self
                     , locator
                     , find_elements=False
                     , iframe_locator=None
                     , timeout=0
                     , stop_test_when_exception=True
                     , refresh_browser_sequence=0
                     , print_not_found_element=True
                     , screen_shot=True
                     ):

        self.browser.switch_to.default_content()  # each time switch to default content
        if iframe_locator is not None:
            if isinstance(iframe_locator, int):
                self.browser.switch_to_frame(iframe_locator)
            elif iframe_locator.startswith("//"):  # xpath
                self.browser.switch_to_frame(self.browser.find_element_by_xpath(iframe_locator))

        return self.__find_elements(locator=locator
                                    , find_elements=find_elements
                                    , timeout=timeout
                                    , stop_test_when_exception=stop_test_when_exception
                                    , refresh_browser_sequence=refresh_browser_sequence
                                    , print_not_found_element=print_not_found_element
                                    , screen_shot=screen_shot
                                    )

    def __find_elements(self
                        , locator
                        , find_elements
                        , timeout=0
                        , stop_test_when_exception=True
                        , refresh_browser_sequence=0
                        , print_not_found_element=True
                        , screen_shot=True):
        stop_test = stop_test_when_exception
        #         self.browser.implicitly_wait(5)
        try:
            if timeout == 0 or refresh_browser_sequence == 0:
                return self.__findelements_softwait(locator, timeout, find_elements)
            else:
                return self.__findelements_refresh(refresh_browser_sequence
                                                   , locator
                                                   , timeout
                                                   , find_elements)
        except:
            return self.find_element_exception(locator
                                               , stop_test_when_exception=stop_test
                                               , print_not_found_element=print_not_found_element,
                                               screen_shot=screen_shot)
        finally:
            self.browser.implicitly_wait(self.default_wait_time)

    def __findelements_softwait(self, locator, timeout, find_elements):
        if find_elements == False:
            elements = self.__find_elem_common(locator, timeout)
        else:
            elements = self.__find_elem_common(locator, timeout, find_elements=True)  # find elements
        self.browser.implicitly_wait(self.default_wait_time)
        return elements

    def __findelements_refresh(self, refresh_browser_sequence, locator, timeout, find_elements):
        if refresh_browser_sequence > timeout:
            raise Exception("refresh_browser_sequence's value should not be more than timeout's value")
        try:
            # self.browser.implicitly_wait(refresh_browser_sequence)
            refresh_browser_times = timeout / refresh_browser_sequence
            last_time_wait = timeout % refresh_browser_sequence
            for i in range(refresh_browser_times):
                try:
                    return self.__findelements_softwait(locator
                                                        , refresh_browser_sequence
                                                        , find_elements)
                except TimeoutException:
                    self.refresh_browser()
                    if i == (refresh_browser_times - 1):
                        if last_time_wait == 0:
                            raise
                        else:
                            return self.__findelements_softwait(locator
                                                                , refresh_browser_sequence + last_time_wait
                                                                , find_elements)
        except:
            raise
        finally:
            self.browser.implicitly_wait(self.default_wait_time)

    def __find_elem_common(self, locator, timeout, find_elements=False):
        by_method = locator[0]
        expression = locator[1]

        if find_elements == False:
            find_method = self.browser.find_element
            elem_wrapper = WebElement_Wrapper
        else:
            find_method = self.browser.find_elements
            elem_wrapper = self.web_elements_wrapper

        try:
            if find_elements == False:
                WebDriverWait(self.browser, timeout).until(
                    expected_conditions.element_to_be_clickable((by_method, expression)))
            else:
                WebDriverWait(self.browser, timeout).until(
                    expected_conditions.presence_of_all_elements_located((by_method, expression)))
        except:
            pass
        finally:
            try:
                elem = find_method(by_method, expression)
                return elem_wrapper(elem, by_method, expression)
            except StaleElementReferenceException:
                print("for StaleElementReferenceException, sleep 5s and then retry %s(%s)" % (
                    find_method.func_name, expression))
                time.sleep(5)
                elem = find_method(by_method, expression)
                return elem_wrapper(elem, by_method, expression)
            except:
                raise

    def find_element_exception(self, locator, stop_test_when_exception=True, print_not_found_element=True,
                               screen_shot=True):
        if stop_test_when_exception:
            raise Exception("[Fail] Go to get Element by %s" % str(locator))
        if print_not_found_element:
            print("[Fail] Go to get Element by %s" % str(locator))
        if screen_shot:
            print("Need add screenshot code")
        return None

    def web_elements_wrapper(self, elem, by_method, expression):
        return [WebElement_Wrapper(e, by_method, expression) for e in elem]

    def take_screen_shot(self, browser):
        dir_name = "C:/Users/xiaos5/Pictures/webdriver/{}".format(
            time.strftime('%Y_%m_%d', time.localtime(time.time())))
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        pic_path = dir_name + "/{}.png".format(time.strftime('%H_%M_%S', time.localtime(time.time())))
        browser.get_screenshot_as_file(pic_path)

    def is_element_appears(self, locator, timeout):
        return WebDriverWait(self.browser, timeout).until(lambda the_driver:
                                                          the_driver.__find_elem_common(locator).is_displayed())

    def disable_javascript_in_html(self):
        self.browser.execute_script("window.onbeforeunload = function() {};")
        self.browser.execute_script("window.alert = function() {};")
        self.browser.execute_script("window.onbeforeunload = function() {};")
        self.browser.execute_script("window.alert = function() {};")

    def back(self):
        """
        Back to old window.

        Usage:
        driver.back()
        """
        self.browser.back()

    def forward(self):
        """
        Forward to old window.

        Usage:
        driver.forward()
        """
        self.driver.forward()

    def move_to_element(self, elem):
        self.actions.move_to_element(elem).perform()
