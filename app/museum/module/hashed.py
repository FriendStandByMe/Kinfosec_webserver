from museum.core.feature import Base
import pickle

class Md5(Base):
    def __init__(self, **kwargs):
        pass

    def process(self, file_path):
        with open(file_path, "rb") as fr:
            data = pickle.load(fr)
        md5_list = data['data']
        return md5_list

    def get_info(self):
        info = "Md5"
        return info
