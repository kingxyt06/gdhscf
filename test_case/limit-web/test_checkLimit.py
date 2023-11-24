import json


class TestCheckLimit:
    def test_chekLimitDate(self,get_agw_token,req_AGW,conf_utill):
        #检查额度的日期
        cookies = get_agw_token
        r = req_AGW
        url = "limit-web/zrlimit/chekLimitDate"
        req_params = conf_utill.config['BASE']['dev']['limit-web']['limit-info']
        res = r.visit(method="POST", url=url, json=req_params, cookies=cookies)
        res = json.loads(res.text)
        assert res['data'] is True


    def test_chekBillCreditIsExist(self,get_agw_token,req_AGW,conf_utill):
        #检查开单额度是否已存在
        cookies = get_agw_token
        r = req_AGW
        url = "limit-web/zrlimit/chekBillCreditIsExist"
        req_params = conf_utill.config['BASE']['dev']['limit-web']['limit-info']
        res = r.visit(method="POST", url=url, json=req_params, cookies=cookies)
        res = json.loads(res.text)
        assert res['code'] == '10001'


