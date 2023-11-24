import json

import pytest


class TestNoticeInfo:
    def test_noticeInfo(self,get_agw_token,req_AGW,get_noticeId):
        notice_id = get_noticeId
        cookies = get_agw_token
        r = req_AGW

        url = f"/sys-web/noticeInfo/detail?id={notice_id}"
        res = r.visit(method="GET", url=url, cookies=cookies)
        res = json.loads(res.text)
        assert res['data'] is not None


    @pytest.fixture()
    def get_noticeId(self,get_agw_token,req_AGW):
        #获取公告列表首个公告id
        cookies = get_agw_token
        r = req_AGW
        url = "sys-web/noticeInfo/pageList"
        req_params = {"current": 1, "size": 10, "queryCondition": {}}
        res = r.visit(method="POST", url=url, json=req_params, cookies=cookies)
        res = json.loads(res.text)
        id = res['data']['records'][0]['id']
        print(f"获取到的公告id是 : {id}")
        yield id
