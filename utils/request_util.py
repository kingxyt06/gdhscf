import json

import requests

from utils.RequestsUtil import RequestsUtil
from utils.YamlUtil import YamlReader

datas = YamlReader().load_data('test_data.yaml')


# for da in datas:
#     caseinfo_keys = da.keys()
#     if 'case' in caseinfo_keys and 'http' in caseinfo_keys and 'expected' in caseinfo_keys:
#         http_keys = da['http'].keys()
#         if 'url' in http_keys and 'method' in http_keys:
#             print("yaml基本架构检查通过")
#             method = da['http'].pop('method')
#             url = da['http'].pop('url')
#             res = RequestsUtil().visit(method=method, url=url, **datas['http'])


class RequestU:
    sess = requests.session()
    def standard_yaml(self):
        datas = YamlReader().load_data('test_data.yaml')
        for da in datas:
            caseinfo_keys = da.keys()
            if 'case' in caseinfo_keys and 'http' in caseinfo_keys and 'expected' in caseinfo_keys:
                http_keys = da['http'].keys()
                if 'url' in http_keys and 'method' in http_keys:
                    print("yaml基本架构检查通过")
                    method = da['http'].pop('method')
                    url = da['http'].pop('url')
                    res = self.send_request(method, url, **da['http'])
                    return_text = res.text


    def send_request(self, method, url, **kwargs):
        method = str(method).upper()
        url = 'https://gdhscf-v2-agw.lianyirong.com.cn/' + url
        # print(kwargs.items())
        for k, v in kwargs.items():
            print(f"{kwargs[k]}的参数替换")
            if k in ['cookies', 'header', 'params']:
                kwargs[k] = self.replace_value(v)
        res = RequestU.sess.request(method, url, **kwargs)
        print(res.cookies)
        print(res.text)
        return res

    def replace_value(self, data):
        if data:
            data_type = type(data)
            # print(f"替换前的类型:{data_type}")
            if isinstance(data, list) or isinstance(data, dict):
                str_data = json.dumps(data)
            else:
                str_data = str(data)
            # print(f"转化过：{str_data}")
            for i in range(1, str_data.count('${') + 1):
                if "${" in str_data and "}" in str_data:
                    start_index = str_data.index("${")
                    end_index = str_data.index("}")
                    old_value = str_data[start_index:end_index + 1]
                    new_value = YamlReader().read_yaml(old_value[2:-1])
                    str_data = str_data.replace(old_value, new_value['cookies'])
                    # print(f"aaa{type(data)}")
                    print(new_value)
            if isinstance(data, dict) or isinstance(data, list):
                data = json.loads(str_data)
            else:
                data = data_type(str_data)
            if isinstance(data, str) and '=' in data and ';' in data:
                data = {item.split('=')[0]: item.split('=')[1] for item in data.split(';')}
        # print(data)
        # print(f"替换后的类型{type(data)}")
        return data


if __name__ == '__main__':
    RequestU().standard_yaml()
