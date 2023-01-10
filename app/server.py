from museum import MUSEUM
from museum.module import AsymmetricExtremum
from requests import get
import os
INDEX_DIR = 'server_dir'
INDEX_NAME = 'app_server'
ES_HOST = get("https://api.ipify.org").text
ES_PORT = 9200

if __name__=='__main__' :

    ms = MUSEUM(host=ES_HOST,port=ES_PORT,use_caching=False)

    ms.create_index(INDEX_NAME,AsymmetricExtremum(window_size=128),num_hash=128,use_smallest=True)
    ms.bulk(INDEX_NAME,os.path.join(os.getcwd(),INDEX_DIR),process_count=8)
