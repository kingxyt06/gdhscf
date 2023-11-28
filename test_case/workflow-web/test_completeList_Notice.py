import json

import pytest


class TestCompleteList_Notice:
    title = ["测试公告标题", "公告", ""]
    context = ["测试公告内容", "内容", ""]

    @pytest.mark.parametrize("title", title)
    @pytest.mark.parametrize("context", context)
    def test_NoticeInfo(self, get_agw_token, req_AGW, title, context):
        # 审批结果查询-公告审批-正向参数用例
        cookies = get_agw_token
        r = req_AGW
        url = "workflow-web/wkfl/export/listCompleteData"
        req_json = {
            "current": 1,
            "size": 10,
            "queryCondition": {
                "extData": {
                    "ext1": title,
                    "ext2": context
                },
                "appTypeList": [
                    "zrNoticeInfo"
                ]
            }
        }
        res = r.visit(method="POST", url=url, cookies=cookies, json=req_json)
        print(res.request.body)
        res = json.loads(res.text)
        assert res['data']['total'] != '0'

    @pytest.mark.parametrize("NotExist_title,NotExist_context",
                             argvalues={("￥%@￥#%", ""), ("", "***&#&@"), ("￥%@￥#%", "***&#&@")})
    def test_NoticeInfo_NotExist(self, get_agw_token, req_AGW,NotExist_title,NotExist_context):
        # 审批结果查询-公告审批-异常参数用例
        cookies = get_agw_token
        r = req_AGW
        url = "workflow-web/wkfl/export/listCompleteData"
        req_json = {
            "current": 1,
            "size": 10,
            "queryCondition": {
                "extData": {
                    "ext1": NotExist_title,
                    "ext2": NotExist_context
                },
                "appTypeList": [
                    "zrNoticeInfo"
                ]
            }
        }
        res = r.visit(method="POST", url=url, cookies=cookies, json=req_json)
        print(res.request.body)
        res = json.loads(res.text)
        assert res['data']['total'] == '0'
