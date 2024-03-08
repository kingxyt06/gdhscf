import json

import pytest

from utils.parameterize_util import read_testcase
from utils.request_util import RequestU

class TestMessageEmailPage:
    # def test_email_pageinfo(self,get_agw_token, req_AGW):
        # req_params = {"current": 1, "size": 10, "queryCondition": {}}
        # r = req_AGW
        # cookies = get_agw_token
        # re = r.visit(method="POST", url="/message-web/messageEmailLog/pageInfo", json=req_params,
        #               cookies=cookies)
        # res = re.json()
        # print(res['data']['records'])

        # 消息通知-邮件信息页面
    @pytest.mark.parametrize('caseinfo', read_testcase('messageEmailPage.yaml'))
    def test_saveAsset(self, caseinfo):
        res = RequestU().standard_yaml(caseinfo)
        print(res)

