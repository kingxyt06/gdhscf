import json

import requests

class TestMessageEmailPage:
    def test_email_pageinfo(self,get_agw_token,req_AGW):
        req_params = {"current":1,"size":10,"queryCondition":{}}
        r = req_AGW
        cookies = get_agw_token
        res = r.visit(method="POST",url="/message-web/messageEmailLog/pageInfo", json=req_params,
                            cookies=cookies)
        res = json.loads(res.text)
        # print(res)
        assert res['data'] is not None


