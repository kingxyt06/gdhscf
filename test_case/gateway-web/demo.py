import json


class TestDemo:
    def test_demo(self, get_agw_token, req_AGW):
        cookies = get_agw_token
        r = req_AGW
        url = '/gateway-web/thirdpartyChannelRelMap/queryExistCfcaProtocol'
        req_params = {
            "applicationFunction": "短信发送",
            "id": "1630092397532954626",
            "channelCode": {"dictParam":"DBASS","displayName":"联易融平台","dictKey":"dbass"}
        }
        res = r.visit(method='POST', url=url, json=req_params, cookies=cookies)
        res = json.loads(res.text)
        print(res)
    def test_demo2(self,get_agw_token, req_AGW):
        cookies = get_agw_token
        r = req_AGW
        url = '/gateway-web/thirdpartyChannelRelMap/getChannelRegister'
        req_params = {
            "applicationFunction": "短信发送",
            "id": "1661634514266046466",
            "channelCode": {"dictParam":"DBASS","displayName":"联易融平台","dictKey":"dbass"}
        }
        res = r.visit(method='POST', url=url, json=req_params, cookies=cookies)
        res = json.loads(res.text)
        print(res)