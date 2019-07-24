import datetime
import unittest

from product.baidu.testcases import test_baidu, test_example
from product.testsuite import html_runner


class  RunDailyRegression(unittest.TestCase):
    def test_run(self):
        report_repository = "C:/Users/xiaobo/Documents/Test_Reports/"
        currentTime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")        
        report = report_repository + currentTime + ".html"
        outfile = open(report, "w")
        runner = html_runner.HTMLTestRunner(
                    stream=outfile,
                    title='Test Report belong Shawn - Daily Regression',
                    description='Regression Test Sample' 
                    )
        my_test_suite = unittest.TestSuite()
        
#         cls_list=[test_baidu.TestBaiDu,test_example.Sample]
#         testcase_list=[]
#         testcases_name=[]
#         for cls in cls_list:
#             testcases_name.append(cls.__name__)
#             testcase_list.append(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
#              
#         my_test_suite.addTests(testcase_list)    
#         print(testcases_name)
        
        my_test_suite.addTests([
                unittest.defaultTestLoader.loadTestsFromTestCase(test_baidu.TestBaiDu)])
        my_test_suite.addTests([
                unittest.defaultTestLoader.loadTestsFromTestCase(test_example.Sample)]) 
         
 
         
         
        for testcases in my_test_suite:
            for testcase in testcases:
                print(testcase.__class__.__name__)
            
        runner.run(my_test_suite)
        outfile.close()


if __name__ == "__main__":
    
    unittest.main()
