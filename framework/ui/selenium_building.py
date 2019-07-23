'''
Created on Aug 7, 2018

@author: xiaos5
'''
from functools import wraps
import time

from selenium.webdriver.common.by import By

# from ui.selenium_libraries import SeleniumLibraries
from framework.ui.selenium_libraries import SeleniumLibraries


def checkpoint(func):
    func._decorators = "checkpoint"

    @wraps(func)
    def wrapper(args):
        print("[Checkpoint] Will do check {}".format(func.__name__).replace("_", " "))
        return func(args)

    return wrapper


def build_webelement(xpath=None, css=None, id=None, class_name=None, tag_name=None, link=None
                     , branch_list=[]
                     , iframe_locator=None
                     , timeout=30
                     , find_elements=False
                     , print_not_found_element_message=True
                     , screen_shot=True
                     , print_time_cost=False
                     ):
    def build_webelement_dec(func):
        parse_branch_locator(func, branch_list, xpath=xpath, css=css, id=id, class_name=class_name, tag_name=tag_name,
                             link=link)

        @wraps(func)
        def build_webelement_wrapped(*args):
            # dont understand
            #             who_call_me =  traceback.extract_stack()[-2][-1]
            #             if "checkpoint_func_for_build_webelement" in who_call_me:
            #                 return func(*args)

            locator = get_current_branch_locator(func)

            if print_time_cost == True:
                start_time = time.time()

            selenium_lib = get_selenium_lib(args)

            actual_element = selenium_lib.find_element(locator
                                                       , find_elements=find_elements
                                                       , iframe_locator=iframe_locator
                                                       , timeout=timeout
                                                       , stop_test_when_exception=False
                                                       , refresh_browser_sequence=0
                                                       , print_not_found_element=print_not_found_element_message
                                                       , screen_shot=screen_shot
                                                       )

            if print_time_cost == True:
                print(
                    "[Total Time Cost] %s (H:M:S)" % (time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))))
            return func(args, actual_element)

        return build_webelement_wrapped

    return build_webelement_dec


def parse_branch_locator(func, branch_list, xpath, css, id, class_name, tag_name, link):
    if branch_list != []:
        if locator_is_for_current_branch(branch_list):
            func.branch_locator = mapping_find_element_method(xpath=xpath, css=css, id=id, class_name=class_name,
                                                              tag_name=tag_name, link=link)
    else:
        if not hasattr(func, "branch_locator"):
            func.common_branch_locator = mapping_find_element_method(xpath=xpath, css=css, id=id, class_name=class_name,
                                                                     tag_name=tag_name, link=link)


def mapping_find_element_method(xpath, css, id, class_name, tag_name, link):
    if xpath is not None:
        return (By.XPATH, xpath)
    elif css is not None:
        return (By.CSS_SELECTOR, css)
    elif id is not None:
        return (By.ID, id)
    elif class_name is not None:
        return (By.CLASS_NAME, class_name)
    elif tag_name is not None:
        return (By.TAG_NAME, tag_name)
    elif link is not None:
        return (By.LINK_TEXT, link)
    else:
        raise Exception("you must tranfer one type of locator from xpath, css or id")


def get_current_branch_locator(func):
    if hasattr(func, "branch_locator"):
        return func.branch_locator
    elif hasattr(func, "common_branch_locator"):
        return func.common_branch_locator
    else:
        raise Exception("\[Automation Rule]\r\n\
        locator of %s() for both current branch and all branch are all not given\r\n\
        make sure your branch_list parameter's value is as below example:\r\n\
        for multiple branches: branch_list=['4.7.000','4.7.100'] \r\n\
        for single branch: branch_list=['4.7.000']\r\n\
        " % func.__name__)


def get_selenium_lib(args):
    try:
        page_object_instance = args[0]
        browser = page_object_instance.browser
        return SeleniumLibraries(browser)
    except AttributeError as err:
        err.message = err.message + "\r\n[Automation rule]\r\n \
        please set browser attribute as below:\r\n \
        import ...\r\n \
        self.browser = browser"
        raise AttributeError(err.message)


def locator_is_for_current_branch(branch_list):
    return False
#     current_branch = ""
#     return current_branch in branch_list
