import pytest
import os

case = "testCase/fanli"

report = "./my_allure_results"

if __name__ == '__main__':
    pytest.main([case, "--alluredir", report, "--capture=no", "--clean-alluredir"])
    os.system('allure serve' + report)

