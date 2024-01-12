import json

import pytest

from utils.YamlUtil import read_testcase
from utils.request_util import RequestU


class TestSaveAsset:

    @pytest.mark.parametrize('caseinfo', read_testcase('saveAssert.yaml'))
    def test_saveAsset(self,caseinfo):
        res = RequestU().standard_yaml(caseinfo)
        print(res)

    @pytest.mark.parametrize('caseinfo', read_testcase('submitApproving.yaml'))
    def test_submitApproving(self, caseinfo):
        res = RequestU().standard_yaml(caseinfo)
        print(res)


