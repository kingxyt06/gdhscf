import json

import pytest


class TestCompleteList_CashApply:
    taskDefKeyList = ["loan_cash_sign_operator",
                      "loan_cash_sign_review",
                      "loan_cash_asset_check",
                      "loan_cash_risk_review"
                      ]
    new_taskDefKey = ()
    for key in taskDefKeyList:
        new_taskDefKey += (key,)
    for i in range(len(taskDefKeyList)):
        for j in range(i + 1, len(taskDefKeyList)):
            new_taskDefKey += ([taskDefKeyList[i], taskDefKeyList[j]],)
    print(new_taskDefKey)


    sedCompanyName = ["广东广垦绿色农产品有限公司", ""]
    @pytest.mark.parametrize("taskDefKeyList", new_taskDefKey)
    @pytest.mark.parametrize("sedCompanyName", sedCompanyName)
    def test_CashApply(self, get_agw_token, req_AGW, taskDefKeyList, sedCompanyName):
        # 审批结果查询-融资审核查询-正向组合

        cookies = get_agw_token
        r = req_AGW
        url = "workflow-web/wkfl/export/listCompleteData"
        req_json = {
            "current": 1,
            "size": 10,
            "queryCondition": {
                "extData": {
                    "ext1": "",
                    "ext6": sedCompanyName,
                },
                "appTypeList": [
                    "zrCashApply"
                ],
                "taskDefKeyList": (lambda x: [x,] if isinstance(x, str) else x)(taskDefKeyList)
            }
        }
        res = r.visit(method="POST", url=url, cookies=cookies, json=req_json)
        print(res.request.body)
        res = json.loads(res.text)
        print(res)
        assert res['data']['total'] is not "0"

    # NotExist_company = ["@#!@#$", ""]
    # NotExist_ext1 = ["TAS-209999999999-999", ""]

    # @pytest.mark.parametrize("NotExist_company", NotExist_company)
    # @pytest.mark.parametrize("NotExist_ext1", NotExist_ext1)
    @pytest.mark.parametrize("NotExist_company,NotExist_ext1",
                             argvalues=[("@#!@#$", ""), ("", "TAS-209999999999-999"), ("@#!@#$", "")])
    @pytest.mark.parametrize("taskDefKeyList", new_taskDefKey)
    def test_CashAppl_NotExistParam(self, get_agw_token, req_AGW, taskDefKeyList, NotExist_company, NotExist_ext1):
        # 审批结果查询-融资审核查询-异常不存在的参数
        cookies = get_agw_token
        r = req_AGW
        url = "workflow-web/wkfl/export/listCompleteData"
        req_json = {
            "current": 1,
            "size": 10,
            "queryCondition": {
                "extData": {
                    "ext1": NotExist_ext1,
                    "ext6":NotExist_company
                },
                "appTypeList": [
                    "zrCashApply"
                ],
                "taskDefKeyList":  (lambda x: [x,] if isinstance(x, str) else x)(taskDefKeyList)
            }
        }
        res = r.visit(method="POST", url=url, cookies=cookies, json=req_json)
        print(res.request.body)
        res = json.loads(res.text)
        print(res)
        assert res['data']['total'] == '0'
