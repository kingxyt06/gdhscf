from config.conf import ConfigReader
from utils.RequestsUtil import RequestsUtil


class ObjectPool:
    def __init__(self):
        self.pool = dict()

    def add_object(self,objs:dict):
        self.pool.update(objs)

    def get_object(self,index:str):
        if len(self.pool) == 0:
            return None
        # print(self.pool)
        return self.pool.get(index)

    def release_object(self,objs:dict):
        self.pool.update(objs)



# if __name__ == '__main__':
#     pools = ObjectPool()
#     r = RequestsUtil()
#     c = ConfigReader()
#     pools.set_object(r, c)
#     pools_list = pools.pool
#     print(pools_list[0])
