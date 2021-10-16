import pytest
import os
from src.tool.get_paths import paths

case = paths.join_path("fanli", "testCase/")
report = paths.join_path("worker_allure_results", "reports/")
allure_results = paths.join_path("allure_results", "reports/")


if __name__ == '__main__':
    pytest.main([case, "--alluredir", report, "--capture=no", "--clean-alluredir"])
    os.system('allure generate {} -o {} --clean'.format(report, allure_results))
    os.system('allure serve' + report)