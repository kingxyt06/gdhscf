import json
import os
import yaml

from utils.YamlUtil import YamlReader


def read_testcase(yaml_name):
    with open(os.getcwd() + "\\"+yaml_name, mode='r', encoding='utf-8') as f:
        caseinfo = yaml.load(f, yaml.FullLoader)
        if 'parameterize' in dict(*caseinfo).keys():
            new_caseinfo = ddt(*caseinfo)
            return new_caseinfo
        else:
            return caseinfo



def ddt(caseinfo):
    if 'parameterize' in caseinfo.keys():
        caseinfo_str = json.dumps(caseinfo)
        for param_key,param_value in caseinfo['parameterize'].items():
            key_list = param_key.split("-")
            data_list = YamlReader().read_data(param_value)
            # 规范yaml数据文件的写法
            length_flag = True
            for data in data_list:
                if len(data) != len(key_list):
                    length_flag = False
                    break
            new_caseinfo = []
            if length_flag:
                for x in range(1, len(data_list)):  # 循环数据的行数
                    temp_caseinfo = caseinfo_str
                    for y in range(0, len(data_list[x])):  # 循环数据列
                        if data_list[0][y] in key_list:
                            # 替换原始的yaml里面的$ddt{}
                            if isinstance(data_list[x][y], int) or isinstance(data_list[x][y], float):
                                temp_caseinfo = temp_caseinfo.replace('"$ddt{' + data_list[0][y] + '}"',
                                                                      str(data_list[x][y]))
                            else:
                                temp_caseinfo = temp_caseinfo.replace("$ddt{" + data_list[0][y] + "}",
                                                                      str(data_list[x][y]))
                    new_caseinfo.append(json.loads(temp_caseinfo))
        return new_caseinfo
    else:
        return caseinfo

