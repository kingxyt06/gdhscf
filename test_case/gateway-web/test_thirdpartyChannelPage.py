import json

from utils.RequestsUtil import RequestsUtil


class TestThirdPartyChannelPage:

    def test_thirdPartyChannelPage(self, get_agw_token, req_utill):
        req_params = {"current": 1, "size": 10, "queryCondition": {}}
        cookies = get_agw_token
        r = req_utill
        url = "gateway-web/thirdpartyChannelRelMap/page"
        res = r.visit(method="POST", url=url, json=req_params, cookies=cookies)
        res = json.loads(res.text)
        assert res['data']['total'] is not None


