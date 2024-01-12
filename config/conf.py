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
        self.config = YamlReader().load_data(self.get_config_file())
        self.env = 'qa'

    def get_config_file(self):
        return config_file

    def get_conf_agw_url(self):
        if self.env == 'dev':
            agw_url = self.config['BASE']['dev']['agw-url']
        elif self.env == 'qa':
            agw_url = self.config['BASE']['qa']['agw-url']
        elif self.env == 'v2':
            agw_url = self.config['BASE']['v2']['agw-url']
        return agw_url

    def get_conf_sp_url(self):
        if self.env == 'dev':
            sp_url = self.config['BASE']['dev']['sp-url']
        elif self.env == 'qa':
            sp_url = self.config['BASE']['qa']['sp-url']
        elif self.env == 'v2':
            sp_url = self.config['BASE']['v2']['sp-url']
        return sp_url

    def get_conf_redis(self):
        if self.env == 'dev':
            redis_url = self.config['BASE']['dev']['redis-url']
        elif self.env == 'qa':
            redis_url = self.config['BASE']['qa']['redis-url']
        elif self.env == 'v2':
            redis_url = self.config['BASE']['v2']['redis-url']
        return redis_url

    def get_redis_db(self):
        if self.env == 'dev':
            redis_db = self.config['BASE']['dev']['redis-db']
        elif self.env == 'qa':
            redis_db = self.config['BASE']['qa']['redis-db']
        elif self.env == 'v2':
            redis_db = self.config['BASE']['v2']['redis-db']
        return redis_db

    def get_conf_mysql(self):
        if self.env == 'dev':
            mysql_url = self.config['BASE']['dev']['mysql-url']
        elif self.env == 'qa':
            mysql_url = self.config['BASE']['qa']['mysql-url']
        return mysql_url

    def get_agw_username(self):
        if self.env == 'dev':
            username = self.config['BASE']['dev']['agw_message']['username']
        elif self.env == 'qa':
            username = self.config['BASE']['qa']['agw_message']['username']
        elif self.env == 'v2':
            username = self.config['BASE']['v2']['agw_message']['username']
        return username

    def get_agw_pwd(self):
        if self.env == 'dev':
            password = self.config['BASE']['dev']['agw_message']['password']
        elif self.env == 'qa':
            password = self.config['BASE']['qa']['agw_message']['password']
        elif self.env == 'v2':
            password = self.config['BASE']['v2']['agw_message']['password']
        return password

    def get_qy_username(self):
        if self.env == 'dev':
            username = self.config['BASE']['dev']['sp_qy_message']['username']
        elif self.env == 'qa':
            username = self.config['BASE']['qa']['sp_qy_message']['username']
        elif self.env == 'v2':
            username = self.config['BASE']['v2']['sp_qy_message']['username']
        return username

    def get_qy_pwd(self):
        if self.env == 'dev':
            password = self.config['BASE']['dev']['sp_qy_message']['password']
        elif self.env == 'qa':
            password = self.config['BASE']['qa']['sp_qy_message']['password']
        elif self.env == 'v2':
            password = self.config['BASE']['v2']['sp_qy_message']['password']
        return password

    def get_conf_checkcode(self):
        return self.config['BASE']['test']['agw_message']['picCheckCode']

    def get_conf_comMessage(self):
        return self.config['BASE']['test']['testCompanyMessage']

    def get_conf_SqlMessage(self):
        return self.config['BASE']['qa']['MySql-Config']


if __name__ == '__main__':
    # r = ConfigReader()
    # url = r.get_conf_mysql()
    sqlConf = ConfigReader().get_conf_SqlMessage()
    print(sqlConf['mysql-url'])
    # print(r.get_conf_sp_url())
