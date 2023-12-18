import json

import pytest


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

    # 测试短信视图参数组合查询
    cust = ["粤海商业保理有限公司", ""]
    receiver = ["17708031513", ""]

    @pytest.mark.parametrize("custName", cust)
    @pytest.mark.parametrize("receiver", receiver)
    def test_Sms_pageinfo_withParams(self, get_agw_token, req_AGW, custName, receiver):
        req_params = {"current": 1, "size": 10, "queryCondition": {"custName": custName, "receiver": receiver,
                                                                   "sendStartDate": "2023-01-01",
                                                                   "sendEndDate": "2023-12-31"}}
        cookies = get_agw_token
        r = req_AGW
        url = "message-web/messageSmsLog/pageInfo"
        res = r.visit(method="POST", url=url, json=req_params,
                      cookies=cookies)
        res = json.loads(res.text)
        assert res['data']['total'] != "0"

    # 测试存量短信数据的发送渠道是LLS
    def test_Sms_historyDataisLLS(self, get_agw_token, req_AGW):
        req_params = {"current": 200, "size": 10, "queryCondition": {}}
        cookies = get_agw_token
        r = req_AGW
        res = r.visit(method="POST", url="message-web/messageSmsLog/pageInfo", json=req_params,
                      cookies=cookies)
        res = json.loads(res.text)
        assert res['data']['records'][0]['channelName'] == 'DBASS'
