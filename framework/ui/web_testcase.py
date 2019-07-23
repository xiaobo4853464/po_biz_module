
import ast
import json
import os
import time
import unittest

from framework.libs.Json_handler import json_get


class WebTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        super(WebTestCase, cls).setUpClass()
    
    @classmethod
    def tearDownClass(cls):
        super(WebTestCase, cls).tearDownClass()
   
    
    def print_test_message(self, expected_value, compared_diff_msg):
        '''
        print the checkpoints' test result as human language
        '''
        for checkpoint, expected in expected_value.items():
            try:
                checkpoint_detail_result = json_get(ast.literal_eval(str(compared_diff_msg).
                                                                     replace("[", "").
                                                                     replace("]", "").
                                                                     replace('"', "")), "$..%s" % checkpoint)
            except:
                checkpoint_detail_result = compared_diff_msg
            pass_the_checkpoint = checkpoint_detail_result is None
            print_message = checkpoint.replace("_", " ")
            if isinstance(expected, bool):
                if expected == False: 
                    print_message = (print_message.replace("is", "is not")
                                  .replace("appear", "not appear")
                                  .replace("exist", "not exist"))
            if  pass_the_checkpoint:
                if isinstance(expected, bool):
                    print ("[Pass check point] check %s" % print_message )
                else:
                    print ("[Pass check point] check %s with [expected_value]--> %s" % (print_message, expected)) 
            else:
                if isinstance(expected, bool):
                    checkpoint_detail_result = ""
                else:
                    checkpoint_detail_result = ("\r\n[compare result]:\r\n" 
                    + json.dumps(checkpoint_detail_result, indent=4, ensure_ascii=False))
                print ("[Fail check point] check %s" % (print_message + checkpoint_detail_result))
                
    def skip_test(self,msg):
        if hasattr(self, 'browser'):
            self.browser.quit()
        self.skipTest(msg)
        
    def assert_equal(self, current_result, expected_result, output_success_msg=None, output_failed_msg=None, **options):
        return self.assert_it(self.assertEqual, (current_result, expected_result), output_success_msg, output_failed_msg, **options)

    def assert_notequal(self, current_result, expected_result, output_success_msg=None, output_failed_msg=None, **options):
        return self.assert_it(self.assertNotEqual, (current_result, expected_result), output_success_msg, output_failed_msg, **options)
    
    def assert_true(self, current_result, output_success_msg=None, output_failed_msg=None, **options):
        return self.assert_it(self.assertTrue, (current_result,), output_success_msg, output_failed_msg, **options)    
    
    def assert_false(self, current_result, output_success_msg=None, output_failed_msg=None, **options):
        return self.assert_it(self.assertFalse, (current_result,), output_success_msg, output_failed_msg, **options)  
    
    def assert_in(self, current_result, in_list, output_success_msg=None, output_failed_msg=None, **options):
        return self.assert_it(self.assertIn, (current_result, in_list), output_success_msg, output_failed_msg, **options) 
        
    def assert_notin(self, current_result, in_list, output_success_msg=None, output_failed_msg=None, **options):
        return self.assert_it(self.assertNotIn, (current_result, in_list), output_success_msg, output_failed_msg, **options)

    def assert_it(self, assert_func, assert_params, output_success_msg=None,
                             output_failed_msg=None, **options):
        '''
        call unittest assert functions and print out the test results.
        if the test is UI test which has self.driver attribute, then it will take screenshot when errors
        
        Usage: in any test case module, assert_func can be any unittest built-in assert method, including: 
          assertEqual, assertNotEqual, assertTrue, assertFalse, assertIn, assertNotIn, ..
          
          You can call assert_it directly, for example for assertEqual:
            assert_it(self.assertEqual, (current_result, expected_result) )
          
          Or you can call there shortcuts methods:
            assert_equal(current_result, expected_result)
                                   
          There is some additional options which can be passed in at the end of parameter list with option=value,
          and here is the option names and default values:
            get_log="light"
            subfolder_name=None
            _print=True
          
        '''
        
        # default options
        get_log="light"
        subfolder_name=None
        _print=True
        
        if options:
            if options.has_key('get_log'):
                get_log = options['get_log']
            if options.has_key('subfolder_name'):
                subfolder_name = options['subfolder_name']
            if options.has_key('_print'):
                _print = options['_print']
                
        # current_result, expected_result
        if len(assert_params) == 1:
            unitary = True
            current_result = assert_params[0]
        elif len(assert_params) == 2:
            unitary = False
            current_result = assert_params[0]
            expected_result = assert_params[1]
        
        try:
            assert_func(*assert_params) 
            if output_success_msg:
                print(output_success_msg)
            
            if unitary:
                print ("[Test Pass] %s success, current result: %s" %  (assert_func.__name__, current_result))
            else:
                if assert_func.__name__ in ['assertIn', 'assertNotIn']:
                    print("[Test Pass] %s success, expected result: %s, in_list: %s" %  (assert_func.__name__, current_result, ' '.join(expected_result)))
                else:
                    print("[Test Pass] %s success, current result: %s, expected result: %s" %  (assert_func.__name__, current_result, expected_result))
        except AssertionError as error:
            print("%s %s" % (assert_func, assert_params) )
            if hasattr(self, 'browser'):
                self.take_screenshot(self.browser)
            # print real value and expected value
            if output_failed_msg:
                print(output_failed_msg)
            
            if unitary:
                print("[Test fail] %s failed, current result: %s" %  (assert_func.__name__, current_result))
            else: 
                if assert_func.__name__ in ['assertIn', 'assertNotIn']:
                    print ("[Test fail] %s failed, current result: %s, in_list: %s" %  (assert_func.__name__, current_result, ' '.join(expected_result)))
                else:
                    print ("[Test fail] %s failed, current result: %s, expected result: %s" %  (assert_func.__name__, current_result, expected_result))
            
            raise error
    
    def assert_operation(self, driver, current_result,
                         expected_result, output_success_msg=None,
                         output_failed_msg=None,screen_shot=True):
    
        try:
            self.assertEqual(current_result, expected_result) 
            if output_success_msg:
                print(output_success_msg)
        except AssertionError as error:
            print("Current assertion result is %s" % current_result)
            if screen_shot:
                self.take_screen_shot(driver)
            if output_failed_msg:
                print(output_failed_msg)
            raise error
    
    
    
    def take_screen_shot(self,browser):
        date_=time.strftime('%Y_%m_%d', time.localtime(time.time()))
        dir_name="C:/Users/xiaos5/Pictures/webdriver/%s"%date_
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        time.sleep(2)
        time_=time.strftime('%H_%M_%S', time.localtime(time.time()))
        pic_path=dir_name+"/%s.png"%time_
        browser.get_screenshot_as_file(pic_path)
        
        print("[Screen shot] Path: %s"%pic_path)

     
