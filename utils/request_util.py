import json
import re

import jsonpath as jsonpath
import requests

from config.conf import ConfigReader
from utils.MysqlUtil import MySQLClient
from utils.YamlUtil import YamlReader, read_testcase


class RequestU:
    sess = requests.session()

    def __init__(self):
        sqlConf = ConfigReader().get_conf_SqlMessage()
        self.sp_url = ConfigReader().get_conf_sp_url()
        self.base_url = ConfigReader().get_conf_agw_url()
        self.session = requests.session()
        self.sqlU = MySQLClient(host=sqlConf['mysql-url'],
                       port=4600,
                       user="root",
                       password="123456"
                       )

    def standard_yaml(self, caseinfo):
        # datas = YamlReader().load_data('test_data.yaml')
        caseinfo_keys = caseinfo.keys()
        if 'method' in caseinfo_keys and 'http' in caseinfo_keys:
            http_keys = caseinfo['http'].keys()
            if 'url' in http_keys and 'cookies' in http_keys:
                print("yaml基本架构检查通过")
                method = caseinfo['method']
                url = caseinfo['http'].pop('url')
                res = self.send_request(method, url, **caseinfo['http'])
                # print(self.sess.cookies)
                return_text = res.text
                return_json = ""
                try:
                    return_json = res.json()
                except Exception as e:
                    print("extract返回的结果不是JSON格式")

                if 'extract' in caseinfo.keys():
                    for k, v in caseinfo['extract'].items():
                        if "(.*?)" in v or "(.+?)" in v or "(\\d+)" in v:
                            zz_value = re.search(v, return_text)
                            if zz_value:
                                extract_value = {k: zz_value.group(1)}
                                YamlReader().write_yaml(extract_value)
                        else:  # jsonpath
                            js_value = jsonpath.jsonpath(return_json, v)
                            if js_value:
                                extract_value = {k: js_value[0]}
                                YamlReader().write_yaml(extract_value)
        res_text = json.loads(return_text)
        return res_text

    def send_request(self, method, url, **kwargs):
        method = str(method).upper()
        # url = self.base_url + url
        if kwargs['client'] == 'agw':
            url = self.base_url + url
            kwargs.pop('client')
        elif kwargs['client'] == 'sp':
            url = self.sp_url + url
            kwargs.pop('client')

        if 'pre_sql' in kwargs and kwargs['pre_sql'] is not None:
            kwargs['pre_sql'] = self.replace_value(kwargs['pre_sql'])
            self.deal_sql(kwargs['pre_sql'])
            kwargs.pop('pre_sql')

        for k, v in kwargs.items():
            if k in ['cookies', 'header', 'params', 'json']:
                kwargs[k] = self.replace_value(v)

        res = RequestU.sess.request(method, url, **kwargs)
        return res

    def replace_value(self, data):
        if data:
            data_type = type(data)
            if isinstance(data, list) or isinstance(data, dict):
                str_data = json.dumps(data)
            else:
                str_data = str(data)
            for i in range(1, str_data.count('${') + 1):
                if "${" in str_data and "}" in str_data:
                    start_index = str_data.index("${")
                    end_index = str_data.index("}")
                    old_value = str_data[start_index:end_index + 1]
                    extract_text = YamlReader().read_yaml(old_value[2:-1])
                    if isinstance(extract_text,(dict,list)):
                        new_value = str(extract_text)
                        str_data = str_data.replace(old_value, new_value)
                    else:
                        str_data = str_data.replace(old_value, extract_text)
                        # print(f"参数{old_value}进行替换后的值:{new_value}")
            if isinstance(data, (dict, list)):
                data = json.loads(str_data)
            elif isinstance(data, str) and '=' in str_data and ';' in str_data:
                data = {item.split('=')[0]: item.split('=')[1] for item in str_data.split(';')}

        # print(f"最后的数据类型是:{type(data)}")
        return data

    def deal_sql(self,yamlSql):
        if isinstance(yamlSql,list):
            for i in yamlSql:
                res = self.sqlU.execute_query(i)
                # print(res)  [proc_inst_id: '3125721']
                sql_result = {}
                if isinstance(res, list):
                    for item in res:
                        sql_result.update(item)
                YamlReader().write_yaml(sql_result)


if __name__ == '__main__':
    caseinfo = read_testcase('test_data.yaml')
    RequestU().standard_yaml(caseinfo)
