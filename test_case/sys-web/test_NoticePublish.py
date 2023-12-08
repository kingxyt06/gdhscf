import json
import time

import pytest


class TestNoticePublish:

    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, get_agw_token, req_AGW, sql_utill):
        global Notice
        # 新建保存一个公告测试数据
        cookies = get_agw_token
        r = req_AGW
        url = "sys-web/noticeInfo/saveOrUpdate"
        req_params = {"publishingObj": ["SUPPLIER", "CORE"], "title": "公告审核-脚本", "content": "公告审核-脚本",
                      "dataChangeHash": "f1nd5ah6"}
        self.announcement = r.visit(method="POST", url=url, json=req_params, cookies=cookies).json()
        # res = json.loads(self.announcement.text)
        print(self.announcement)
        id = self.announcement['data']['id']
        print(f"新建的公告id是 : {id}")
        Notice = self.announcement
        yield Notice
        # sqlU.select_database("gdhscf_sys")
        # result = sqlU.execute_query(f"update notice_info set enable = 0  where id = {Notice['data']['id']}")

    def test_NoticePublish(self, get_agw_token, req_AGW):
        # 新增的公告-提交审批
        cookies = get_agw_token
        r = req_AGW
        url = "sys-web/noticeInfo/startProcess"
        params = {
            "noticeId": Notice['data']['id'],
            "status": "PUBLISHED",
            "processType": "zrNoticeInfo"
        }
        res = r.visit(method="POST", url=url, cookies=cookies, params=params)
        res = json.loads(res.text)
        assert res['message'] == "OK"

    def test_NoticeClaim(self, get_agw_token, req_AGW, sql_utill):
        # 公告审批-公告领取
        cookies = get_agw_token
        r = req_AGW
        sqlU = sql_utill
        sqlU.select_database("gdhscf_workflow")

        # 设定轮训去访问直到工作流能查询到
        max_attempts = 10
        attempt = 1
        # print("Attempt:", attempt, "Max Attempts:", max_attempts)
        #
        # print(f"select * from wkfl_app_main where business_id = '{Notice['data']['id']}'")

        while True:
            result = sqlU.execute_query(
                f"select * from wkfl_app_main where business_id = '{Notice['data']['id']}'")
            if len(result) == 1:
                # print(result)
                break
            elif attempt <= max_attempts:
                time.sleep(1)
                attempt += 1
            else:
                print("error")
                break

        proc_inst_id = result[0]['proc_inst_id']
        # 公告审核-领取任务
        taskId = sqlU.execute_query(
            f'''
                select
	                ID_
                from
                    act_ru_task art
                inner join wkfl_app_main wam on
                    art.PROC_INST_ID_ = wam.proc_inst_id
                where
                    art.PROC_INST_ID_ = '{proc_inst_id}' 
            ''')

        # print(taskId[0]['ID_'])
        url = "workflow-web/wkfl/workbench/claim"
        params = {'taskId': taskId[0]['ID_']}
        res = r.visit(method="POST", url=url, cookies=cookies, params=params)
        res = json.loads(res.text)
        assert res['code'] == '200'


    def test_NoticeFinish(self,get_agw_token,req_AGW,sql_utill):
        #公告审核-办理通过
        cookies = get_agw_token
        r = req_AGW
        sqlU = sql_utill
        #前置步骤: 获取公告测试数据的taskId
        result = sqlU.execute_query(
            f"select * from wkfl_app_main where business_id = '{Notice['data']['id']}'")
        proc_inst_id = result[0]['proc_inst_id']
        taskId = sqlU.execute_query(
            f'''
                        select
        	                ID_
                        from
                            act_ru_task art
                        inner join wkfl_app_main wam on
                            art.PROC_INST_ID_ = wam.proc_inst_id
                        where
                            art.PROC_INST_ID_ = '{proc_inst_id}' 
                    ''')
        taskId = taskId[0]['ID_']

        data = {
            'taskId': taskId,
            'auditState': '通过',
            'comment': '',
            'json': '{}'
        }
        url = '/workflow-web/wkfl/workbench/completeTask'
        res = r.visit(method="POST",url=url,data=data,cookies=cookies)
        res = json.loads(res.text)
        assert res['code'] == '200'




