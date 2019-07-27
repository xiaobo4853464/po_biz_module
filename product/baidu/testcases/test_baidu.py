'''
Created on Aug 8, 2018

@author: xiaos5
'''

import unittest

from framework.ui.page_object_testcase import get_testdata_dec, PageObjectTestCase
from product.baidu.modules.baidu import Baidu


class TestBaiDu(PageObjectTestCase):
    """
    a doc for test
    """

    def setUp(self):
        self.browser = self.start_browser("Chrome")
        self.test_module = Baidu(self.browser)
        if self.test_module.go_to_page() == False:
            raise unittest.TestCase("[Skip] go to page failed!")

    @get_testdata_dec(input_values=True)
    def test_default(self, testdata):
        expect_data = testdata[0]
        input_data = testdata[1]
        input_box = self.test_module.search_box()
        input_box.send_keys(input_data["test_input"])
        self.biz_module_test(expect_data,expect_data)

    # #         btn.click()
    # #         btn.click_by_js()
    #         self.biz_module_test(expect_data)

    def tearDown(self):
        self.browser.quit()


if __name__ == '__main__':
    unittest.main()
