import json
import os
import time

import allure
import pytest
from redis import Redis

from config.conf import ConfigReader

# from utils.Encryption import get_publicKey, Encryption
from utils.ObjectPool import ObjectPool
from utils.RequestsUtil import RequestsUtil

# from utils.SqlUtil import MysqlDb
# from utils.common import CommonUtil



# 获取配置信息
# companyMessage = ConfigReader().get_conf_comMessage()
# 实例化公共方法对象
# ComUtil = CommonUtil()
# sqlConf = ConfigReader().get_conf_SqlMessage()


# def get_verifyCode():
#     code_url = 'captcha-web/captcha/code/get'
#     rsp = r.visit(method="GET", url=code_url)
#     data = rsp.cookies
#     data = requests.utils.dict_from_cookiejar(data)
#     CAPTCHAID = 'CAPTCHAID' + '=' + data['CAPTCHAID']
#     headers = {
#         "content-type": "application/json",
#         "Cookie": CAPTCHAID
#     }
#     captcha_url = 'sys-web/user/getCaptchaCode'
#     rsp = r.visit(method="POST", url=captcha_url, headers=headers).json()
#     print(rsp['data'])
#     return rsp['data']


# @allure.title("前置步骤----创建测试专用的额度信息")
# @pytest.fixture(scope="class")
# def createLimitForTest(agw_login):
#     url = "limit-web/limit/saveApplyLimitInfo"
#     cookies = agw_login
#     req_json = {
#         "applyLimitName": "yt自动生成测试额度",
#         "companyId": companyMessage['CompanyId'],
#         "limitType": "overallCredit",
#         "fundId": companyMessage['fundId'],
#         "recyclable": "YES",
#         "applyAmount": "500000",
#         "startDate": ComUtil.NowDate,
#         "expireDate": ComUtil.NowDate,
#         "dataChangeHash": "f2vj1h8r",
#         "creditPeriod": "1",
#         "fundName": companyMessage['fundName'],
#         "companyName": companyMessage['CompanyName'],
#         "companyNo": companyMessage['CompanyNo'],
#         "relateLimitCompanyId": "1552476100802203649",
#         "relateLimitCompanyName": "yt测试-核心企业",
#         "limitTypeName": "综合额度",
#         "approvalAmount": "500000",
#         "applyType": "NEW",
#         "companyType": "CORE_SUB"
#     }
#     rsp = r.visit(method="POST", url=url, json=req_json, cookies=cookies)
#     # print(rsp.request.url)
#     rsp = json.loads(rsp.text)
#     # print(rsp)
#     print(f"\n前置步骤-----创建测试专用的额度信息编号:%s" % rsp['data']['limitApplyNo'])
#
#     yield rsp['data']
#
#     mysql_db = MysqlDb(host=sqlConf['host'], port=sqlConf['port'], user=sqlConf['user'], password=sqlConf['password'],
#                        db_name=sqlConf['db_name']['limit-db'])
#     print("\n开始清除测试额度数据")
#     mysql_db.execute_db(f"delete from apply_limit_info where limit_apply_no='%s'" % rsp['data']['limitApplyNo'])
#     mysql_db.execute_db(f"delete from apply_sub_limit where limit_apply_no='%s'" % rsp['data']['limitApplyNo'])
#     mysql_db.execute_db(f"delete from limit_info where app_lmt_no ='%s'" % rsp['data']['limitApplyNo'])
#     mysql_db.execute_db(f"delete from limit_info where parent_lmt_no ='%s'" % rsp['data']['limitApplyNo'])



@pytest.fixture(scope="session", autouse=True)
def init_pools():
    pools = ObjectPool()
    # 实例化两个类，并放进去
    r = RequestsUtil()
    c = ConfigReader()
    pools.add_object({'reqU':r})
    pools.add_object({'confU':c})
    print(f"------------初始化对象池啦-----------:\n{pools.pool}")
    return pools

# @pytest.fixture(scope="session", autouse=True)
# def object_pools(init_pools):
#     # 实例化两个类，并放进去
#     r = RequestsUtil()
#     c = ConfigReader()
#     init_pools.add_object({'reqU':r})
#     init_pools.add_object({'confU':c})
#     # 定义变量接收这个对象池，并返回
#     pools_list = init_pools.pool
#     print(f"------------拿到对象池啦-----------:\n{pools_list}")
#     return pools_list

@pytest.fixture(scope="session", autouse=True)
def req_utill(init_pools):
    return init_pools.get_object('reqU')


@pytest.fixture(scope="session", autouse=True)
def conf_utill(init_pools):
    return init_pools.get_object('confU')

# @pytest.fixture()
# def getinstance():
#     reqU = RequestsUtil()
#     confR = ConfigReader()
#     return [reqU,confR]
#
# @pytest.fixture()
# def objectPools(getinstance):
#     pools = getinstance
#     return pools




@pytest.fixture(scope="session")
def get_agw_token(init_pools,req_utill,conf_utill):
    print("\n前置步骤----获取登录cookie")
    global token
    # print(object_pools.get('confU'))
    redis_url = conf_utill.get_conf_redis()
    rds = Redis(host=redis_url, port='6379', password='', decode_responses=True, db=116)
    captcha_data = {'timestamp': int(round(time.time() * 1000))}
    url = "tools-web/captcha/code/get"
    res = req_utill.visit(method="GET", url=url, params=captcha_data)
    picCheckCodeKey = res.cookies.get_dict()['CAPTCHAID']
    # print(res.cookies.get_dict())
    picCheckCode = rds.get(picCheckCodeKey)[1:5]
    print("登陆验证码为 : " + picCheckCode)
    username = conf_utill.get_agw_username()
    password = conf_utill.get_agw_pwd()
    login_params = {
        "password": password,
        "picCheckCode": picCheckCode,
        "userName": username
    }
    headers = {'Content-Type': 'application/json;charset=UTF-8', 'Content-Length': '0'}
    cookies = {'CAPTCHAID': picCheckCodeKey}
    login_url = "sys-web/user/login"
    login_res = req_utill.visit(method="POST", url=login_url, json=login_params, headers=headers,
                        cookies=cookies)
    # print(login_res.json())
    token = login_res.cookies
    print("登录成功----获取token成功")
    return token

# if __name__ == '__main__':
#     get_agw_token()
