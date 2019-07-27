'''
Created on Aug 9, 2018

@author: xiaos5
'''

from framework.ui.selenium_building import build_webelement, checkpoint
from product.baidu.pages.baidu_page import BaiduPage


class Baidu(BaiduPage):
    def __init__(self, browser):
        self.browser = browser

    def go_to_page(self):
        self.browser.get(self.url)
        return "baidu" in self.browser.current_url.lower()

    @build_webelement(id='kw')
    def search_box(self, element):
        return element

    @build_webelement(id='kw_tip')
    def search_box_after_input(self, element):
        return element

    @build_webelement(css=".bg.s_btn_wr>.bg.s_btn")
    def search_btn(self, element):
        return element

    @checkpoint
    def search_box_appears(self):
        return self.search_box() is not None

    @checkpoint
    def search_box_importable(self):
        try:
            self.search_box().send_keys("hello world!")
            return True
        except:
            return False
