'''
Created on Aug 22, 2018

@author: xiaos5
'''
from ui.selenium_building import build_webelement

class BugzillaMysticTask():
    def __init__(self,browser,base_url="https://bugzilla.vp.lab.emc.com/",usr=None,pwd=None):
        self.browser=browser
        self.base_url=base_url
        self.usr=usr
        self.pwd=pwd
        
    
    def go_to_page(self,url):
        self.browser.get(self.base_url)
        if "log in" in self.login_btn().text.lower():
            self.do_login()
        self.browser.get(url)
        return url in self.browser.current_url
    
    @build_webelement(id="account")
    def login_btn(self,element):
        return element
    
    @build_webelement(id="Bugzilla_login")
    def usr_box(self,element):
        return element
        
    @build_webelement(id="Bugzilla_password")
    def pwd_box(self,element):
        return element
    
    @build_webelement(id="log_in")
    def login_confirm_btn(self,element):
        return element
    
    def do_login(self):
        self.login_btn().click()
        self.usr_box().send_keys(self.usr)
        self.pwd_box().send_keys(self.pwd)
        self.login_confirm_btn().click()
    
    
        
                