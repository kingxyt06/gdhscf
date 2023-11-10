import json

import pytest


class TestNoticePage:
    status = ["UNPUBLISHED", "PUBLISHED", "SOLD_OUT"]
    auditStatus = ["INIT", "CHECKING", "PASS", "REJECT"]
    publishingObj = ["SUPPLIER", "CORE"]

    def test_noticePage(self, get_agw_token, req_utill):
        # 公告页面列表页
        cookies = get_agw_token
        r = req_utill
        url = "sys-web/noticeInfo/pageList"
        req_params = {"current": 1, "size": 10, "queryCondition": {}}
        res = r.visit(method="POST", url=url, json=req_params, cookies=cookies)
        res = json.loads(res.text)
        assert res['data']['total'] is not None

    @pytest.mark.parametrize("publishingObj", publishingObj)
    @pytest.mark.parametrize("status", status)
    @pytest.mark.parametrize("auditStatus", auditStatus)
    def test_noticePage_query(self, get_agw_token, req_utill, publishingObj, status, auditStatus):
        # 查询条件组合-公告页面列表页

        condition = {"titleOrContent": "测试", "publishingObj": publishingObj, "status": status,
                     "auditStatus": auditStatus}
        req_params = {"current": 1, "size": 10, "queryCondition": condition}
        cookies = get_agw_token
        r = req_utill
        url = "sys-web/noticeInfo/pageList"
        res = r.visit(method="POST", url=url, json=req_params, cookies=cookies)
        res = json.loads(res.text)
        assert res['data']['total'] is not None
