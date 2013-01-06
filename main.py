'''
Created on Aug 9, 2012

@author: gausscheng
'''


from ic_test.ic_built_in_tester import ICActionTester


if __name__ == '__main__':
#    f = open("IMMTestCaseCloseMold.yml")
#    x = yaml.load(f)
#    print (x)
    action_test_case = ICActionTester()
    action_test_case.load(open("IMMTestCaseCloseMold.yml", mode='r').read())
    action_test_case.run_case()
    print (action_test_case.test_report())
