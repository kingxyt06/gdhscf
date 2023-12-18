import os.path

import yaml


class YamlReader:
    def __init__(self):
        self._data = None
        self._data_all = None

    def load_data(self,yamlf):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError("文件不存在")
        if not self._data:
            with open(self.yamlf, "rb") as f:
                self._data = yaml.safe_load(f)
                return self._data

    # def data(self):
    #     if not self._data:
    #         with open(self.yamlf, "rb") as f:
    #             self._data = yaml.safe_load(f)
    #             return self._data

    def data_all(self):
        if not self._data_all:
            with open(self.yamlf, "rb") as f:
                self._data_all = yaml.safe_load_all(f)
                return self._data_all

    def write_yaml(self, data):
        with open(os.getcwd() + '/extract.yaml', mode="a") as f:
            yaml.dump(data, stream=f, allow_unicode=True)
