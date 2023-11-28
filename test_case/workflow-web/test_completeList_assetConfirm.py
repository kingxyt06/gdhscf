import json

import pytest


class TestCompleteList_assetConfirm:
    appNo = ["202305221500004709", "2023", ""]
    companyName = ["tyl测试开单额度-核心", ""]
    taskDefKeyList = [
        "asset_open_sign_review",
        "asset_open_risk_review",
        "asset_open_check",
        "asset_open_sign_operator"
    ]
    new_taskDefKey = ()
    for key in taskDefKeyList:
        new_taskDefKey += (key,)
    for i in range(len(taskDefKeyList)):
        for j in range(i + 1, len(taskDefKeyList)):
            new_taskDefKey += ([taskDefKeyList[i], taskDefKeyList[j]],)

    recv_cust = ["yt供应商二号",""]
    appNo = ["202311271400005734","20231127",""]

    @pytest.mark.parametrize("appNo",appNo)
    @pytest.mark.parametrize("recvCust",recv_cust)
    @pytest.mark.parametrize("taskDefKeyList", new_taskDefKey)
    def test_assetConfirm(self,get_agw_token, req_AGW,taskDefKeyList,recvCust,appNo):
        #审批结果查询-开立审核-正向参数用例
        cookies = get_agw_token
        r = req_AGW
        url = "workflow-web/wkfl/export/listCompleteData"
        req_json = {
            "current": 1,
            "size": 10,
            "queryCondition": {
                "appNo": appNo,
                "extData": {
                    "ext1": recvCust
                },
                "appTypeList": [
                    "assetConfirm"
                ],
                "taskDefKeyList": (lambda x: [x, ] if isinstance(x, str) else x)(taskDefKeyList)
            }
        }
        res = r.visit(method="POST", url=url, cookies=cookies, json=req_json)
        print(res.request.body)
        res = json.loads(res.text)
        assert res['data']['total'] != '0'

    error_cust = ["$%@$!","yt"]
    error_No = ["209999999900009999","9999",""]

    @pytest.mark.parametrize("error_No",error_No)
    @pytest.mark.parametrize("error_cust",error_cust)
    @pytest.mark.parametrize("taskDefKeyList", new_taskDefKey)
    def test_assetConfirm_NoExist(self,get_agw_token, req_AGW,taskDefKeyList,error_No,error_cust):
        #审批结果查询-开立审核-异常参数用例
        cookies = get_agw_token
        r = req_AGW
        url = "workflow-web/wkfl/export/listCompleteData"
        req_json = {
            "current": 1,
            "size": 10,
            "queryCondition": {
                "appNo": error_No,
                "extData": {
                    "ext1": error_cust
                },
                "appTypeList": [
                    "assetConfirm"
                ],
                "taskDefKeyList": (lambda x: [x, ] if isinstance(x, str) else x)(taskDefKeyList)
            }
        }
        res = r.visit(method="POST", url=url, cookies=cookies, json=req_json)
        print(res.request.body)
        res = json.loads(res.text)
        assert res['data']['total'] == '0'