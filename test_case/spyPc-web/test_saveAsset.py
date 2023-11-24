import json


class TestSaveAsset:
    def test_saveAsset(self, get_sp_token_qy, req_SP, conf_utill):
        cookies = get_sp_token_qy
        r = req_SP
        url = "spyPc-web/asset/saveAsset"
        req_params = conf_utill.config['BASE']['dev']['asset-info']
        print(req_params)
        res = r.visit(method="POST", url=url, json=req_params, cookies=cookies)
        res = json.loads(res.text)
        assert res['data']['assetNo'] is not None


