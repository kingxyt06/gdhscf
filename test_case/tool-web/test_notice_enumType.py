
import json

import pytest


class TestEnumType_notice:
    # 测试公告查询页面的枚举值
    req_data = (
        {'enumType': "NoticeStatusEnum"}, {'enumType': 'NoticeAuditStatusEnum'},
        {'enumType': 'NoticePublishingObjEnum'})

    @pytest.mark.parametrize('data', req_data)
    def test_NoticeStatusEnum(self, get_agw_token, req_AGW, data):
        # 公告状态,发布对象,审核状态  三个枚举值检查
        cookies = get_agw_token
        r = req_AGW
        url = 'tools-web/enumType/queryList'
        req_params = data
        res = r.visit(method='POST', url=url, json=req_params, cookies=cookies)
        res = json.loads(res.text)
        assert res['data'] is not None
