import json
from datetime import datetime

import pytest


class TestNoticePullOut:

    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, sql_utill):
        # 前置步骤: 插入一条已发布状态的公告数据，用于下架测试
        global notice_id
        sqlU = sql_utill
        sqlU.select_database("gdhscf_sys")
        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        published_sql = f"""
        INSERT INTO gdhscf_sys.notice_info (publishing_obj,title,status,audit_status,content,enable,create_id,create_name,create_time,update_id,update_name,update_time,process_status) VALUES
('01,02', '已上架公告-sql插入', 'PUBLISHED', 'PASS', '已上架公告-sql插入', 1, 1727599716125061121, '自动化专用', '{formatted_time}',
 1727599716125061121, '自动化专用', '{formatted_time}', 'PUBLISHED')
                            """
        try:
            sqlU.execute_query(published_sql)
        except sqlU.IntegrityError as e:
            print(f"Insert failed: {e}")

        res = sqlU.execute_query(
            "select * from gdhscf_sys.notice_info where title='已上架公告-sql插入'and status = 'PUBLISHED' order by create_time DESC limit 1")
        if res:
            print(res[0]['id'])
            self.notice_id = res[0]['id']
        else:
            print("No results found.")
        notice_id = self.notice_id
        yield notice_id
        # sqlU.execute_query(f"update notice_info set enable = 0  where id = '{Notice}'")

    def test_NoticePullOut(self, get_agw_token, req_AGW):
        # 公告管理-提交下架请求
        url = '/sys-web/noticeInfo/startProcess'
        cookies = get_agw_token
        r = req_AGW
        params = {
            "noticeId": notice_id,
            "status": "SOLD_OUT",
            "processType": "zrNoticeInfo"
        }
        res = r.visit(method="POST", url=url, cookies=cookies, params=params)
        res = json.loads(res.text)
        assert res['message'] == "OK"

    def test_NoticePullOut_claim(self, get_agw_token, req_AGW, sql_utill):
        # 公告审批-领取下架任务
        cookies = get_agw_token
        r = req_AGW
        sqlU = sql_utill
        sqlU.select_database("gdhscf_workflow")
        result = sqlU.execute_query(
            f"select * from wkfl_app_main where business_id = '{notice_id}'")
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
        url = "workflow-web/wkfl/workbench/claim"
        params = {'taskId': taskId[0]['ID_']}
        res = r.visit(method="POST", url=url, cookies=cookies, params=params)
        res = json.loads(res.text)
        assert res['code'] == '200'

    def test_NoticeFinish(self, get_agw_token, req_AGW, sql_utill):
        # 公告审批-审批下架-办理通过
        cookies = get_agw_token
        r = req_AGW
        sqlU = sql_utill
        # 前置步骤: 获取公告测试数据的taskId
        result = sqlU.execute_query(
            f"select * from wkfl_app_main where business_id = '{notice_id}'")
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
        res = r.visit(method="POST", url=url, data=data, cookies=cookies)
        res = json.loads(res.text)
        assert res['code'] == '200'
