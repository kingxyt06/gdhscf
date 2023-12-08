import json

import requests

from utils.RequestsUtil import RequestsUtil


class TestMessageSmsPage:
    # 短信全视图默认页面
    def test_Sms_pageinfo(self, get_agw_token, req_AGW):
        req_params = {"current": 1, "size": 10, "queryCondition": {}}
        cookies = get_agw_token
        r = req_AGW
        url = "message-web/messageSmsLog/pageInfo"
        res = r.visit(method="POST", url=url, json=req_params,
                      cookies=cookies)
        res = json.loads(res.text)
        assert res['data'] is not None

    # 测试存量短信数据的发送渠道是LLS
    def test_Sms_historyDataisLLS(self, get_agw_token, req_AGW):
        req_params = {"current": 200, "size": 10, "queryCondition": {}}
        cookies = get_agw_token
        r = req_AGW
        res = r.visit(method="POST", url="message-web/messageSmsLog/pageInfo", json=req_params,
                      cookies=cookies)
        res = json.loads(res.text)
        assert res['data']['records'][0]['channelName'] == 'DBASS'
