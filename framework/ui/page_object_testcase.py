'''
Created on Aug 10, 2018

@author: xiaos5
'''
from collections import OrderedDict
import inspect
import os
from functools import wraps
from selenium import webdriver

# from libs.Json_handler import json_get, jsonFile_get, assertJson
# from ui.web_testcase import WebTestCase
from framework.libs.Json_handler import json_get, jsonFile_get, assertJson
from framework.ui.web_testcase import WebTestCase


def get_expected_value_dec(func):
    @wraps(func)
    def wrapped(args):
        all_testdata = get_testdata(args)
        jsonpath_for_expected = "$..expected_values"
        testdata = json_get(all_testdata, jsonpath_for_expected) or all_testdata
        return func(args, testdata)

    return wrapped


def get_testdata_dec(input_values=False):
    def get_testdata_decorator(func):
        stack = inspect.stack()
        frame = stack[1]

        @wraps(func)
        def wrapped(args):
            all_testdata = get_testdata(args)
            jsonpath_for_expected = "$..expected_values"
            expect_data = json_get(all_testdata, jsonpath_for_expected) or all_testdata
            testdata = expect_data
            if input_values:
                jsonpath_for_input = "$..input_values"
                input_data = json_get(all_testdata, jsonpath_for_input)
                testdata = (expect_data, input_data)
            return func(args, testdata)

        return wrapped

    return get_testdata_decorator


def get_input_data(self):
    all_testdata = self.get_testdata()
    jsonpath_for_input = "$..input_values"
    return json_get(all_testdata, jsonpath_for_input) or all_testdata


def get_testdata(obj):
    test_data_dir_path = (os.path.dirname(inspect.getfile(obj.__class__))
                          .replace("testcases", "testdata"))
    test_module_name = obj.test_module.__class__.__name__.lower()
    test_data_path = test_data_dir_path + '\\' + test_module_name + ".json"
    expr_with_testcase = "$..%s" % obj._testMethodName.lower()
    testdata = jsonFile_get(test_data_path, expr_with_testcase)

    current_branch = "4.5.300"  # sample
    if current_branch:
        current_branch = 'branch_' + current_branch.replace('.', '_')
        branch_group = current_branch[0:10] + '_all'
    else:
        current_branch = " "
        branch_group = " "
    priority_list = [current_branch, branch_group, "common"]
    testdata_with_branch = json_get_with_priority(testdata, priority_list) or testdata

    # with platform
    platform = "windows"  # sample
    expr_with_platform = "$..%s" % platform
    testdata_with_platform = json_get(testdata_with_branch, expr_with_platform) or testdata_with_branch

    return testdata_with_platform


class PageObjectTestCase(WebTestCase):
    def start_browser(self, browser_name="firefox"):
        if browser_name.lower() == "firefox":
            browser = webdriver.Firefox()
        elif browser_name.lower() == "chrome":
            browser = webdriver.Chrome()
        browser.maximize_window()
        return browser

    def get_input_data(self):
        all_testdata = self.get_testdata()
        jsonpath_for_input = "$..input_values"
        return json_get(all_testdata, jsonpath_for_input) or all_testdata

    def get_expected_value(self):
        '''
        it will get the testdata from [biz_module].json 
        from a key whose name is the same with unittest's test case method 
        '''
        all_testdata = self.get_testdata()
        jsonpath_for_expected = "$..expected_values"
        testdata = json_get(all_testdata, jsonpath_for_expected) or all_testdata
        if testdata is None:
            raise BaseException("please confirm your data in file %s could be gotten with jsonpath %s" \
                                % (self.testdata_file_path, "$..%s" % self._testMethodName))
        return testdata

    def get_testdata(self):
        #         localProjectPath = get_project_path()
        testdata_project_path = (os.path.dirname(inspect.getfile(self.__class__))
                                 .replace("testcases", "testdata"))
        test_module = (self.test_module.__class__.__name__).lower()
        test_data_path = testdata_project_path + '\\' + test_module + ".json"
        expr_with_testcase = "$..%s" % self._testMethodName.lower()
        testdata = jsonFile_get(test_data_path, expr_with_testcase)

        current_branch = "4.5.300"  # sample
        if current_branch:
            current_branch = 'branch_' + current_branch.replace('.', '_')
            branch_group = current_branch[0:10] + '_all'
        else:
            current_branch = " "
            branch_group = " "
        priority_list = [current_branch, branch_group, "common"]
        testdata_with_branch = json_get_with_priority(testdata, priority_list) or testdata

        # with platform
        platform = "windows"  # sample
        expr_with_platform = "$..%s" % platform
        testdata_with_platform = json_get(testdata_with_branch, expr_with_platform) or testdata_with_branch

        return testdata_with_platform

        '''
    Feature1:
        expected value contains checkpoints info
        est_module.get_actual_value will go to get the actual values of the checkpoints abstracted from expected value
        how to get the actual value?
        call the method whose names are same with checkpoints in expected value from [biz_module].py
    Feature2:
        auto print these checkpoints descritpion to html report with human lanuguage
    Feature3:
        auto sreen shot when comparing expected with actual fails
    Feature4:
        auto show the difference of expected and acutal if fails
    '''

    def biz_module_test(self, expected_value, test_module=None, browser=None, ignore_compare_order=False):
        test_module = test_module or self.test_module
        if hasattr(self, 'browser'):
            browser = browser or self.browser
        actual_value = self.get_actual_value(expected_value=expected_value)
        test_result, detail_diff = assertJson(expected_value, actual_value, ignore_compare_order=ignore_compare_order)
        self.print_test_message(expected_value, detail_diff)  # TBD
        if browser == None:
            self.assert_operation(browser, test_result, True, "[Test Result] Pass", "[Test Result] Fail",
                                  screen_shot=False)
        else:
            self.assert_operation(browser, test_result, True, "[Test Result] Pass", "[Test Result] Fail",
                                  screen_shot=True)

    def get_actual_value(self, expected_value=None):
        '''
        expected value contains checkpoints info
            est_module.get_actual_value will go to get the actual values of the checkpoints abstracted from expected value
            how to get the actual value?
            call the method whose names are same with checkpoints in expected value from [biz_module].py
        '''
        actual_value, has_sub_biz_module = self.get_actual_value_format(expected_value)
        #         if expected_value == None: return self.get_all_checkPoint_(self)
        for checkpoint, checkpoint_expected_value in expected_value.items():
            checkpoint_fun = self.test_module.__getattribute__(checkpoint)
            if has_sub_biz_module == False:
                actual_value[checkpoint] = checkpoint_fun()
            else:
                expected_value_sub_biz_module_example = checkpoint_expected_value
                if isinstance(checkpoint_expected_value, list):
                    expected_value_sub_biz_module_example = checkpoint_expected_value[0]
                expected_value_sub_biz_module_format = \
                    self.get_actual_value_format(expected_value_sub_biz_module_example)[0]
                actual_value[checkpoint] = checkpoint_fun(expected_value_sub_biz_module_format)
        return actual_value

    def get_actual_value_format(self, expected_value):
        actual = OrderedDict(expected_value)
        has_sub_biz_module = False
        for k, v in actual.items():
            if isinstance(v, list) and not (isinstance(v[0], str) or isinstance(v[0], bytes)):
                actual[k] = [self.get_actual_value_format(v[0])]
                has_sub_biz_module = True
            elif not isinstance(v, dict):
                actual[k] = None
        return actual, has_sub_biz_module

    def disable_javascript_in_html(self, browser):
        browser.execute_script("window.onbeforeunload = function() {};")
        browser.execute_script("window.alert = function() {};")
        browser.execute_script("window.onbeforeunload = function() {};")
        browser.execute_script("window.alert = function() {};")


def get_project_path():
    originPath = os.path.dirname(__file__)
    if "VxRailManager" in originPath:
        return originPath.split("VxRailManager")[0] + "VxRailManager/"
    elif "VMB_Test" in originPath:
        return originPath.split("VMB_Test")[0] + "VMB_Test/"
    elif "vxrailtest" in originPath:
        return originPath.split("vxrailtest")[0]
    else:
        return originPath


def json_get_with_priority(json_content, priority_list):
    priority = 0
    while priority < len(priority_list):
        xpath = json_get(json_content, '$..%s' % priority_list[priority])
        if xpath != None:
            return xpath
        priority += 1
    return None
