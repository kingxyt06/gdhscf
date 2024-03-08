import json

import pytest

from utils.YamlUtil import read_testcase
from utils.request_util import RequestU


class TestSaveAsset:

    # 新增导入资产
    @pytest.mark.parametrize('caseinfo', read_testcase('saveAssert.yaml'))
    def test_saveAsset(self, caseinfo):
        res = RequestU().standard_yaml(caseinfo)
        print(res)

    # 提交资产
    @pytest.mark.parametrize('caseinfo', read_testcase('submitApproving.yaml'))
    def test_submitApproving(self, caseinfo):
        res = RequestU().standard_yaml(caseinfo)
        print(res)

    # 工作台-领取任务
    @pytest.mark.parametrize('caseinfo', read_testcase('claimTask.yaml'))
    def test_chaimTask(self, caseinfo):
        res = RequestU().standard_yaml(caseinfo)
        print(res)

    # 工作台-退领任务
    @pytest.mark.parametrize('caseinfo', read_testcase('unclaimTask.yaml'))
    def test_unchaimTask(self, caseinfo):
        res = RequestU().standard_yaml(caseinfo)
        print(res)
