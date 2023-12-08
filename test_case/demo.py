
if __name__ == '__main__':
    taskDefKeyList = ["loan_cash_sign_operator",
                      "loan_cash_sign_review",
                      "loan_cash_asset_check",
                      "loan_cash_risk_review"
                      ]
    from config.conf import ConfigReader
    from utils.MysqlUtil import MySQLClient


    #
    # result = ()
    #
    # for key in taskDefKeyList:
    #     result += (key,)
    # for i in range(len(taskDefKeyList)):
    #     for j in range(i + 1, len(taskDefKeyList)):
    #         result +=([taskDefKeyList[i], taskDefKeyList[j]],)
    # print(result)

    # com_json = {
    #     "current": 1,
    #     "size": 10,
    #     "queryCondition": {
    #         "appNo": "",
    #         "extData": {
    #             "ext1": ""
    #         },
    #         "appTypeList": [
    #             "zrCustSelfApply", "zrCustApplyNonAuto"
    #         ],
    #         "taskDefKeyList": ""
    #     }
    # }
    # com_json.update({"queryCondition":{"taskDefKeyList": (lambda x: [x, ] if isinstance(x, str) else x)(taskDefKeyList)}})
    # com_json['queryCondition']['taskDefKeyList']=(lambda x: [x,] if isinstance(x, str) else x)(taskDefKeyList)
    # print(com_json['queryCondition']['taskDefKeyList'])
    # print(type(com_json))

    sqlConf = ConfigReader().get_conf_SqlMessage()
    sqlclient = MySQLClient(host=sqlConf['mysql-url'],
                            user="root",
                            password=123456
                            )

    sqlclient.select_database("gdhscf_workflow")
    res = sqlclient.execute_query(f"select * from wkfl_app_main where app_No = '202312051700006219'")
    print(res)
