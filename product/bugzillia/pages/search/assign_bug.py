'''
Created on Aug 22, 2018

@author: xiaos5
'''
import traceback

from ui.selenium_building import build_webelement, checkpoint
from bugzillia.pages.search.seach_advance_page import SearchAdvancePage
from bugzillia.pages.search.search_result import Search_Result

class Assign_Bug(SearchAdvancePage):
    def __init__(self,browser,usr,pwd,comment,first_status):
        self.browser=browser
        self.usr=usr
        self.comment=comment
        self.first_status=first_status
        super().__init__(browser=self.browser,usr=self.usr,pwd=pwd)
        self.sr=Search_Result(browser=self.browser,usr=self.usr,pwd=pwd)
        
    
    def go_to_page(self):
        self.sr.go_to_page()
        self.first_bug=self.sr.first_bug()
        return self.first_bug is not None
    
    @build_webelement(id='bz_assignee_edit_action')
    def assign_to_edit_btn(self,element):
        return element
    
    @build_webelement(xpath="//*[@name='assigned_to']")
    def assign_to_input_box(self,element):
        return element
    
    @build_webelement(id='comment')
    def comments_text(self,element):
        return element
    
    @build_webelement(id='bug_status')
    def status_selector(self,element):
        return element
    
    @build_webelement(id='resolution')
    def resolve_status_selector(self,element):
        return element
    
    @build_webelement(id='commit')
    def save_changes_btn(self,element):
        return element
    
    @build_webelement(xpath="//*[@class='navigation']//a[text()='Next']")
    def next_bug(self,element):
        return element
    
    @checkpoint
    def assign_success(self):
        try:
            self.first_bug.click()
            self.assign_operation(self.usr,self.comment,self.first_status)
            print("All bugs has been assigto '%s'"%self.usr)
            return True
        except Exception:
            traceback.print_exc()
            return False
    
    def assign_operation(self,usr,comment,first_status):
        while True:
            self.assign_to_edit_btn().click()
            self.assign_to_input_box().send_keys(usr)
            self.comments_text().send_keys(comment)
            slct=self.status_selector().selector()
            slct.select_by_value(first_status)
            slct_resolve=self.resolve_status_selector().selector()
            slct_resolve.select_by_value("FIXED")
            self.save_changes_btn().click()
            
            next_bug_link=self.next_bug()
            if next_bug_link is not None:
                next_bug_link.click()
            else:
                break
        