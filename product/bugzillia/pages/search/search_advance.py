'''
Created on Aug 22, 2018

@author: xiaos5
'''
from bugzillia.pages.search.seach_advance_page import SearchAdvancePage
from ui.selenium_building import build_webelement, checkpoint


class Search_Advance(SearchAdvancePage):
    def __init__(self,browser,usr,pwd):
        self.browser=browser
        super().__init__(browser=self.browser,usr=usr,pwd=pwd)
    
    def go_to_page(self):
        return super().go_to_page(url=self.url)
    
    @build_webelement(id='email1')
    def first_search_box(self,element):
        return element
    
    @build_webelement(xpath="//*[@id='people_filter']/a")
    def search_by_people_link(self,element):
        return element
    
    @checkpoint
    def search_by_people_link_appears(self):
        return self.search_by_people_link() is not None