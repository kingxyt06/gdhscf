import json

import pytest


class TestNoticeDel:

    def test_NoticeDel(self, get_agw_token, req_AGW,create_Notice):
        cookies = get_agw_token
        r = req_AGW
        notice_id = create_Notice
        url=f"sys-web/noticeInfo/deleteById?id={notice_id}"
        res = r.visit(method="POST", url=url, cookies=cookies)
        res = json.loads(res.text)
        assert res['data'] is True

    @pytest.fixture()
    def create_Notice(self, get_agw_token, req_AGW):
        cookies = get_agw_token
        r = req_AGW
        url = "sys-web/noticeInfo/saveOrUpdate"
        req_params = {"publishingObj": ["SUPPLIER", "CORE"], "title": "由脚本新增", "content": "由脚本新增",
               "dataChangeHash": "f1nd5ah6"}
        res = r.visit(method="POST", url=url, json=req_params, cookies=cookies)
        res = json.loads(res.text)
        id = res['data']['id']
        print(f"新建的公告id是 : {id}")
        yield id
