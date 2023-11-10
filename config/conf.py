import datetime
import os
import time

from utils.YamlUtil import YamlReader

current_path = os.path.abspath(__file__)
# print(current_path)
BASE_DIR = os.path.dirname(os.path.dirname(current_path))
config_path = BASE_DIR + os.sep + "config"
config_file = config_path + os.sep + "config.yaml"
# print(config_file)
#
# data_path = BASE_DIR + os.sep + "test_data"
# data_file = data_path + os.sep + "data.yaml"



time_ = datetime.datetime.now().strftime("%Y-%m-%d")
# print(time_)


#
# def get_config_file():
#     return config_file

class ConfigReader:
    def __init__(self):
        self.config_file = config_path + os.sep + "config.yaml"
        self.config = YamlReader(self.get_config_file()).data()
        self.env = 'dev'

    def get_config_file(self):
        return config_file

    def get_conf_agw_url(self):
        if self.env == 'dev':
            agw_url = self.config['BASE']['dev']['agw-url']
        elif self.env == 'test':
            agw_url = self.config['BASE']['test']['agw-url']
        return agw_url

    def get_conf_sp_url(self):
        if self.env == 'dev':
            sp_url = self.config['BASE']['dev']['sp-url']
        elif self.env == 'test':
            sp_url = self.config['BASE']['test']['sp-url']
        return sp_url

    def get_conf_redis(self):
        if self.env == 'dev':
            redis_url = self.config['BASE']['dev']['redis-url']
        elif self.env == 'test':
            redis_url = self.config['BASE']['test']['redis-url']
        return redis_url

    def get_agw_username(self):
        if self.env == 'dev':
            username = self.config['BASE']['dev']['agw_message']['username']
        elif self.env == 'test':
            username = self.config['BASE']['test']['agw_message']['username']
        return username

    def get_agw_pwd(self):
        if self.env == 'dev':
            password = self.config['BASE']['dev']['agw_message']['password']
        elif self.env == 'test':
            password = self.config['BASE']['test']['agw_message']['password']
        return password

    def get_sp_username(self,type):
        if type == 'qy':
            username = self.config['BASE']['test']['sp_message_qy']['username']
        elif type == 'gys':
            username = self.config['BASE']['test']['sp_message_gys']['username']
        return username

    def get_sp_pwd(self,type):
        if type == 'qy':
            password = self.config['BASE']['test']['sp_message_qy']['password']
        elif type == 'gys':
            password = self.config['BASE']['test']['sp_message_gys']['password']
        return password



    def get_conf_checkcode(self):
        return self.config['BASE']['test']['agw_message']['picCheckCode']

    def get_conf_comMessage(self):
        return self.config['BASE']['test']['testCompanyMessage']

    def get_conf_SqlMessage(self):
        return self.config['BASE']['test']['MySql-Config']

if __name__ == '__main__':
    r = ConfigReader()
    url = r.get_conf_agw_url(env='test')
    print(url)
    # print(r.get_conf_sp_url())

