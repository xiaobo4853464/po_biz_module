'''
Created on Aug 23, 2018

@author: xiaos5
'''
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from bugzillia.pages.search.seach_advance_page import SearchAdvancePage
from bugzillia.pages.search.search_advance import Search_Advance
from ui.selenium_building import build_webelement, checkpoint


class Search_Result(SearchAdvancePage):
    def __init__(self,browser,usr,pwd):
        self.browser=browser
        self.usr=usr
        self.sa=Search_Advance(browser=self.browser,usr=self.usr,pwd=pwd)
        super().__init__(browser=self.browser,usr=self.usr,pwd=pwd)
    
    def go_to_page(self):
        self.sa.go_to_page()
        if self.sa.first_search_box().is_displayed()==False:
            self.sa.search_by_people_link().click()
        self.sa.first_search_box().send_keys(self.usr)
        act=ActionChains(self.browser)
        act.send_keys(Keys.ENTER).perform()
        
        return self.assignee_person_appears()
        
    
    @build_webelement(xpath="//*[@class='search_description']")
    def assignee_person(self,element):
        return element
    
    @build_webelement(xpath="//*[@class='first-child bz_id_column']//a")
    def first_bug(self,elements):
        return elements
    
    @checkpoint
    def assignee_person_appears(self):
        return self.assignee_person() is not None
    
    @build_webelement(xpath="//*[@class='bz_result_count']")
    def bugs_elem(self,element):
        return element
    
    def bugs_count(self):
        bugs=self.bugs_elem()
        if bugs is not None:
            return bugs.text
        else:
            return 0      