'''
Created on Aug 22, 2018

@author: xiaos5
'''
import unittest

from selenium import webdriver

from bugzillia.pages.search.assign_bug import Assign_Bug
from bugzillia.pages.search.search_advance import Search_Advance
from bugzillia.pages.search.search_result import Search_Result
from bugzillia.testdata import test_data
from ui.page_object_testcase import PageObjectTestCase, get_expected_value_dec


class TestBugzillaBugClose(PageObjectTestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser=webdriver.Chrome()
        cls.browser.implicitly_wait(3)
        cls.browser.maximize_window()
        
        td=test_data.DATA
        u_k="zhongqi"
        cls.usr=td["usr"][u_k]
        cls.pwd=td["pwd"][u_k]
        cls.comment=td["comment"][u_k]
        cls.first_status=td["first_status"][u_k]
        
        
        
    def setUp(self):
        self.testcase_name=self._testMethodName.lower()
        testcase_name=self.testcase_name
        
        if "wizard0" in testcase_name:
            self.test_module=Search_Advance(browser=self.browser,usr=self.usr,pwd=self.pwd)
        elif "wizard1" in testcase_name:
            self.test_module=Search_Result(browser=self.browser,usr=self.usr,pwd=self.pwd)
        elif "wizard2" in testcase_name:
            self.test_module=Assign_Bug(browser=self.browser,usr=self.usr,pwd=self.pwd,comment=self.comment,first_status=self.first_status)
        if self.test_module.go_to_page()==False:
            self.skipTest("[SKIP] go to page failed!")
        
    @get_expected_value_dec
    def test_wizard0_search(self,testdata):
        self.biz_module_test(testdata)
    
    @get_expected_value_dec
    def test_wizard1_search_result(self,testdata):
        self.biz_module_test(testdata)
    
    @get_expected_value_dec
    def test_wizard2_assign_bug(self,testdata):
        self.biz_module_test(testdata)
        
    
    
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
    
if __name__ == '__main__':
    unittest.main()