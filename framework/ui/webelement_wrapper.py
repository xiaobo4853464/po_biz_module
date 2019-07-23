'''
Created on Aug 15, 2018

@author: xiaos5
'''
from functools import wraps
import traceback

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select


def print_call_msg_decorator(func):

    @wraps(func)
    def wrapped(*arg):
        call_from_method_info = traceback.extract_stack()[-2][-1]
        if "send_keys" in call_from_method_info:
            data = arg[-1]
            if "\n" in data:
                temp=list(data)
                index=data.index("\n")
                temp.pop(index)
                temp.insert(index, '\\n')
                data="".join(temp)
#             call_from_method = call_from_method_info.split(".")[-2]
            call_from_method = call_from_method_info.split("(")[0].split(".")
            for i in call_from_method:
                if "self"!=i:
                    call_from_method=i
            msg = "[Test Step] Send '%s' to '%s'" % (data, call_from_method)
        else:
#             call_from_method = call_from_method_info.split(".")[-2].split("()")[0].replace("_", " ")
            call_from_method = call_from_method_info.split(".")[-2].strip("()").replace("_", " ")
            msg = "[Test Step] Click '%s'" % call_from_method
        msg = msg.replace("()", "")
        print(msg)
        func(*arg)

    return wrapped


class WebElement_Wrapper():

    def __init__(self, element, by=None, locator=None):
        self.elem = element
        self.by = by
        self.locator = locator
        self.browser = self.elem.parent
        self.act = ActionChains(self.browser)
        
    def __getattr__(self, attr):
        return getattr(self.elem, attr)
    
    @print_call_msg_decorator
    def click(self):
        try:
            self.elem.click()
        except:
            traceback.print_exc()
    
    @print_call_msg_decorator
    def send_keys(self, data, clear_flag=True):
        try:
            if clear_flag:
                self.elem.clear()
            self.elem.send_keys(data)
        except:
            traceback.print_exc()

    def selector(self):
        return Select(self.elem)
    
    @print_call_msg_decorator
    def click_by_js(self):
        by = self.by
        locator = self.locator
        if by.lower() == "xpath":
            js = "document.evaluate(\"%s\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue" % locator
        elif by.lower() == "css selector":
            js = "document.querySelector('%s')" % locator
        elif by.lower() == "id":
            js = "document.getElementById('%s')" % locator
        elif by.lower() == "class name":
            js = "document.getElementsByClassName('%s')" % locator
        elif by.lower() == "tag name":
            js = "document.getElementsByTagName('%s')" % locator
        
        js = js + ".click()"
        self.browser.execute_script(js)
    
    
