from utils.RequestsUtil import RequestsUtil
from utils.YamlUtil import YamlReader

datas = YamlReader().load_data('test_data.yaml')
for da in datas:
    caseinfo_keys = da.keys()
    if 'case' in caseinfo_keys and 'http' in caseinfo_keys and 'expected' in caseinfo_keys:
        http_keys = da['http'].keys()
        if 'url' in http_keys and 'method' in http_keys:
            print("yaml基本架构检查通过")
            method = da['http'].pop('method')
            url = da['http'].pop('url')
            path = da['http'].pop('path')
            res = RequestsUtil().visit(method=method,url=path,**datas['http'])

class requestU:

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
                    res = RequestsUtil().visit(method=method, url=url, **datas['http'])



    def send_request(self,method,url,**kwargs):
    #
