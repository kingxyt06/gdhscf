import json

import pytest


class TestCompleteList_LimitApply:
    custs = ['凌渊科技有限公司', '企业', '']
    ltNos = ['LT-2023052503853', 'LT', '']

    @pytest.mark.parametrize("custName", custs)
    @pytest.mark.parametrize("lt_No", ltNos)
    def test_LimitApply(self, get_agw_token, req_AGW, custName, lt_No):
        # 审批结果查询-额度审核查询-正向参数组合
        cookies = get_agw_token
        r = req_AGW
        url = "workflow-web/wkfl/export/listCompleteData"
        req_json = {
            "current": 1,
            "size": 10,
            "queryCondition": {
                "extData": {
                    "ext6": custName,
                    "ext5": lt_No
                },
                "appTypeList": [
                    "zrLimitApply"
                ]
            }
        }
        res = r.visit(method="POST", url=url, cookies=cookies, json=req_json)
        print(res.request.body)
        res = json.loads(res.text)
        assert res['data']['total'] is not None

    @pytest.mark.parametrize("error_cust,error_no",
                             argvalues=[("#￥%@", ""), ("", "LT-2999999909999"), ("#￥%@", "LT-2999999909999")])
    def test_LimitApply_NotExist(self, get_agw_token, req_AGW, error_cust, error_no):
        # 审批结果查询-额度审核查询-异常参数组合
        cookies = get_agw_token
        r = req_AGW
        url = "workflow-web/wkfl/export/listCompleteData"

        req_json = {
            "current": 1,
            "size": 10,
            "queryCondition": {
                "extData": {
                    "ext6": error_cust,
                    "ext5": error_no
                },
                "appTypeList": [
                    "zrLimitApply"
                ]
            }
        }
        res = r.visit(method="POST", url=url, cookies=cookies, json=req_json)
        res = json.loads(res.text)
        assert res['data']['total'] == '0'
