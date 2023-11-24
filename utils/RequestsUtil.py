import requests as requests

from config.conf import ConfigReader


class RequestsUtil:

    def __init__(self, url_type="agw"):
        self.url_type = url_type
        # self.agw_ip = ConfigReader().get_conf_agw_url()
        # print("\n当前内管端域名:"+self.agw_ip)
        # self.sp_ip = ConfigReader().get_conf_sp_url()
        # print("当前客户端域名:" + self.sp_ip)
        # self.session = requests.session()
        if  self.url_type == "agw":
            self.agw_ip = ConfigReader().get_conf_agw_url()
            print("\n当前内管端域名:" + self.agw_ip)
        else:
            self.sp_ip = ConfigReader().get_conf_sp_url()
            print("当前客户端域名:" + self.sp_ip)
        self.session = requests.session()




    def visit(self, method, url, params=None, data=None, json=None, cookies=None, headers=None, **kwargs):
        if self.url_type == 'agw':
            return self.session.request(method=method, url=self.agw_ip + url, params=params, data=data, json=json,
                                        cookies=cookies, headers=headers, **kwargs)
        else:
            return self.session.request(method=method, url=self.sp_ip + url, params=params, data=data, json=json,
                                        cookies=cookies, headers=headers, **kwargs)

    def close_session(self):
        self.session.close()

    # def __del__(self):
    #     print("------------------开始关闭session------------------")
    #     self.session.close()
