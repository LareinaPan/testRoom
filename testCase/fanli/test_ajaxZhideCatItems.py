import allure
import pytest
from api.fanliApi import *


@allure.feature("返利")
@allure.story("返利-homepage")
class TestAjaxZhideCatItems:

    @allure.title("接口校验")
    def test_ajaxZhideCatItems(self):
        res = get_ajaxZhideCatItems()


if __name__ == "__main__":
    pytest.main(["-svx"])


