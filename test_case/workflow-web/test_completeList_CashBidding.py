import json

import pytest


class TestCompleteList_CashBidding:
    appNo = ["202305221500004709", "2023", ""]
    companyName = ["tyl测试开单额度-核心", ""]
    taskDefKeyList = [
        "cash_bidding_first",
        "cash_bidding_second"
    ]
    new_taskDefKey = ()
    for key in taskDefKeyList:
        new_taskDefKey += (key,)
    for i in range(len(taskDefKeyList)):
        for j in range(i + 1, len(taskDefKeyList)):
            new_taskDefKey += ([taskDefKeyList[i], taskDefKeyList[j]],)

    @pytest.mark.parametrize("appNo", appNo)
    @pytest.mark.parametrize("companyName", companyName)
    @pytest.mark.parametrize("taskDefKeyList", new_taskDefKey)
    def test_cashBidding(self, get_agw_token, req_AGW, appNo, companyName, taskDefKeyList):
        # 审批结果查询-报价审核查询-正向参数组合
        cookies = get_agw_token
        r = req_AGW
        url = "workflow-web/wkfl/export/listCompleteData"
        req_json = {
            "current": 1,
            "size": 10,
            "queryCondition": {
                "appNo": appNo,
                "extData": {
                    "ext2": companyName
                },
                "appTypeList": [
                    "zrCashBiddingApply"
                ],
                "taskDefKeyList": (lambda x: [x, ] if isinstance(x, str) else x)(taskDefKeyList)
            }
        }
        res = r.visit(method="POST", url=url, cookies=cookies, json=req_json)
        print(res.request.body)
        res = json.loads(res.text)
        assert res['data']['total'] != '0'

    error_appNo = ["209999999900009999", "9999", ""]
    error_companyName = ["！#~@#", "tyl"]
    @pytest.mark.parametrize("error_appNo", error_appNo)
    @pytest.mark.parametrize("error_companyName", error_companyName)
    @pytest.mark.parametrize("taskDefKeyList", new_taskDefKey)
    def test_cashBidding_NoExist(self, get_agw_token, req_AGW, error_appNo, error_companyName, taskDefKeyList):
        # 审批结果查询-报价审核查询-异常参数组合
        cookies = get_agw_token
        r = req_AGW
        url = "workflow-web/wkfl/export/listCompleteData"
        req_json = {
            "current": 1,
            "size": 10,
            "queryCondition": {
                "appNo": error_appNo,
                "extData": {
                    "ext2": error_companyName
                },
                "appTypeList": [
                    "zrCashBiddingApply"
                ],
                "taskDefKeyList": (lambda x: [x, ] if isinstance(x, str) else x)(taskDefKeyList)
            }
        }
        res = r.visit(method="POST", url=url, cookies=cookies, json=req_json)
        print(res.request.body)
        res = json.loads(res.text)
        assert res['data']['total'] == '0'
