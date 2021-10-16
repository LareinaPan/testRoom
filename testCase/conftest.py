import pytest
import allure
from api.fanliApi import *

# 返利-homepage
@allure.step("返利-homepage")
@pytest.fixture()
def ajaxZhideCatItems(request):
    kws = request.param
    res = get_ajaxZhideCatItems(**kws)
    return res