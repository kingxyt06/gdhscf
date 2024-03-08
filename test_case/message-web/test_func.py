import pytest

from utils.YamlUtil import read_testcase
from utils.request_util import RequestU


class TestFunc:
    pass

    @pytest.mark.parametrize('caseinfo', read_testcase('test_data.yaml'))
    def test_func(self, caseinfo):
        res = RequestU().standard_yaml(caseinfo)
        print(res)
