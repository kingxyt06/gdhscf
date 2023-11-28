import json

import pytest


class TestCompleteList_CustUpdate:
    appNo = ["202311", ""]
    companyName = ["yt供应商一号", "yt", "$#!%@#%!", ""]
    taskDefKeyList = ["usr_manager", "usr_director"]
    new_taskDefKey = ()
    for key in taskDefKeyList:
        new_taskDefKey += (key,)
    for i in range(len(taskDefKeyList)):
        for j in range(i + 1, len(taskDefKeyList)):
            new_taskDefKey += ([taskDefKeyList[i], taskDefKeyList[j]],)
    print(new_taskDefKey)

    @pytest.mark.parametrize("appNo", appNo)
    @pytest.mark.parametrize("companyName", companyName)
    @pytest.mark.parametrize("taskDefKeyList", new_taskDefKey)
    def test_CustUpdate(self, get_agw_token, req_AGW, appNo, companyName, taskDefKeyList):
        # 审批结果查询-企业变更查询-正向参数组合
        cookies = get_agw_token
        r = req_AGW
        url = "workflow-web/wkfl/export/listCompleteData"
        req_json = {
            "current": 1,
            "size": 10,
            "queryCondition": {
                "appNo": appNo,
                "extData": {
                    "ext1": companyName
                },
                "appTypeList": [
                    "zrCustSelfApply", "zrCustApplyNonAutoUpdate"
                ],
                "taskDefKeyList": (lambda x: [x, ] if isinstance(x, str) else x)(taskDefKeyList)
            }
        }

        res = r.visit(method="POST", url=url, cookies=cookies, json=req_json)
        print(res.request.body)
        res = json.loads(res.text)
        print(res)
        assert res['data'] is not None

    @pytest.mark.parametrize("taskDefKeyList", new_taskDefKey)
    def test_NotExistCust(self, get_agw_token, req_AGW, taskDefKeyList):
        # 审批结果查询-企业变更查询-输入不存在的企业名称查询
        NotExistCust = "#$@%!^#"
        cookies = get_agw_token
        r = req_AGW
        url = "workflow-web/wkfl/export/listCompleteData"
        req_json = {
            "current": 1,
            "size": 10,
            "queryCondition": {
                "appNo": "",
                "extData": {
                    "ext1": NotExistCust
                },
                "appTypeList": [
                    "zrCustSelfApply", "zrCustApplyNonAutoUpdate"
                ],
                "taskDefKeyList": (lambda x: [x, ] if isinstance(x, str) else x)(taskDefKeyList)
            }
        }
        res = r.visit(method="POST", url=url, cookies=cookies, json=req_json)
        print(res.request.body)
        res = json.loads(res.text)
        print(res)
        assert res['data']['total'] == '0'

    @pytest.mark.parametrize("taskDefKeyList", new_taskDefKey)
    def test_NotExistAppNo(self, get_agw_token, req_AGW, taskDefKeyList):
        # 审批结果查询-企业变更查询-输入不存在appNo
        NotExistAppNo = "299911241000005691"
        cookies = get_agw_token
        r = req_AGW
        url = "workflow-web/wkfl/export/listCompleteData"
        req_json = {
            "current": 1,
            "size": 10,
            "queryCondition": {
                "appNo": NotExistAppNo,
                "extData": {
                    "ext1": ""
                },
                "appTypeList": [
                    "zrCustSelfApply", "zrCustApplyNonAutoUpdate"
                ],
                "taskDefKeyList": (lambda x: [x, ] if isinstance(x, str) else x)(taskDefKeyList)
            }
        }
        res = r.visit(method="POST", url=url, cookies=cookies, json=req_json)
        print(res.request.body)
        res = json.loads(res.text)
        print(res)
        assert res['data']['total'] == '0'

    # def test_completeList_CustUpdate_other(self,get_agw_token, req_AGW):
    #     cookies = get_agw_token
    #     r = req_AGW
    #     url = "workflow-web/wkfl/export/listCompleteData"
    #     NotExistAppNo = "299911241000005691"
    #     NotExistCust = "#$@%!^#"
    #     req_json = {
    #         "current": 1,
    #         "size": 10,
    #         "queryCondition": {
    #             "appNo": NotExistAppNo,
    #             "extData": {
    #                 "ext1": NotExistCust
    #             },
    #             "appTypeList": [
    #                 "zrCustSelfApply", "zrCustApplyNonAutoUpdate"
    #             ],
    #             "taskDefKeyList": [
    #                 "usr_manager", "usr_director"
    #             ]
    #         }
    #     }
    #     res = r.visit(method="POST", url=url, cookies=cookies, json=req_json)
    #     print(res.request.body)
    #     res = json.loads(res.text)
    #     print(res)
    #     assert res['data']['total'] == '0'
