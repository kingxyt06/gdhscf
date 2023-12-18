import json

import pytest


class TestTsTradePage:
    transactionType = ["TRANSFER","CASH"]
    @pytest.mark.parametrize("type",transactionType)
    def test_tsTradePage(self, get_agw_token, req_AGW,type):
        cookies = get_agw_token
        r = req_AGW
        url = "transaction-web/tsTrade/page"
        req_params = {
            "current": 1,
            "size": 10,
            "queryCondition": {
                "transactionType": type
            }
        }
        res = r.visit(method='POST', url=url, json=req_params, cookies=cookies)
        res = json.loads(res.text)
        assert res['data'] is not None


    def test_tsTradePage_paramsR(self):
        pass
