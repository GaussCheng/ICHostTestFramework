'''
Created on Aug 9, 2012

@author: gausscheng
'''


from ic_test_case.ic_built_in_test_case import ICActionTestCase


if __name__ == '__main__':
#    f = open("IMMTestCaseCloseMold.yml")
#    x = yaml.load(f)
#    print (x)
    action_test_case = ICActionTestCase()
    action_test_case.load(open("IMMTestCaseCloseMold.yml", mode='r').read())
    action_test_case.run_case()
    print (action_test_case.test_report())
