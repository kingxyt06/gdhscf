import json

import pytest


class TestChangeChannelCA:
    # 电子签章配置DBASS,GDHCAPITAL(粤海资本平台)
    channel_list = ['DBASS', 'GDHCAPITAL']

    @pytest.mark.parametrize('channel', channel_list)
    def test_changeChanel_sms(self, get_agw_token, req_AGW, recover_channel_ca, channel):
        init_conf = recover_channel_ca
        cookies = get_agw_token
        r = req_AGW

        url = "gateway-web/thirdpartyChannelRelMap/changingOver"
        req_params = {"applicationFunction": "电子签章", "channelCode": channel}
        res = r.visit(method="POST", url=url, json=req_params, cookies=cookies)
        # print(res.request.body)
        res = json.loads(res.text)
        assert res['data'] == True
        # 恢复初始配置
        recover_param = {"applicationFunction": "电子签章", "channelCode": init_conf}
        recover_conf = r.visit(method="POST", url=url, json=recover_param, cookies=cookies)
        assert recover_conf.status_code == 200
        # print(recover_conf)

    @pytest.fixture()
    def recover_channel_ca(self, get_agw_token, req_AGW):
        # 获取当前的电子签章配置渠道，后面用作复原用
        cookies = get_agw_token
        r = req_AGW
        req_params = {"current": 1, "size": 10, "queryCondition": {}}
        page_url = "gateway-web/thirdpartyChannelRelMap/page"
        page_res = r.visit(method="POST", url=page_url, json=req_params, cookies=cookies)
        page_res = json.loads(page_res.text)
        init_channel = page_res['data']['records'][0]['channelCode']
        init_conf = json.loads(init_channel)
        print(init_conf['dictParam'])
        yield init_conf['dictParam']
