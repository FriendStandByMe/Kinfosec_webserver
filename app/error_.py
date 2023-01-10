from museum import MUSEUM
import ssdeep
import os
from museum import MUSEUM
from museum.module import AsymmetricExtremum
import time
from tqdm import tqdm
from requests import get
import time
import pickle
import random
import warnings
warnings.filterwarnings('ignore')

ES_HOST = get("https://api.ipify.org").text
ES_PORT = 9200
INDEX = 'app_server'
QUERY_DIR1 = 'query_data1'
QUERY_DIR2 = 'query_data2'
QUERY_DIR3 = 'query_data3'
INDEX_DIR = 'index_data'
def ex4_ex() :
    query_dir = os.path.join(os.getcwd(), QUERY_DIR3)
    index_dir = os.path.join(os.getcwd(), INDEX_DIR)
    ms = MUSEUM(host=ES_HOST, port=ES_PORT, use_caching=False)
    lists_in = os.listdir(index_dir)
    lists_ = os.listdir(query_dir)
    ssdeep_time = []

    for query_file in lists_ :
        path = os.path.join(query_dir, query_file)
        a = ssdeep.hash_from_file(path)
        x = time.time()
        result = ms.search(INDEX, path, limit=50)
        result_time = time.time() - x
        vi_list = []
        for hit in result['hits']:
            if hit['estimated_similarity'] == 0 :
                os.remove(path)
                break

def ex4() :
    query_dir = os.path.join(os.getcwd(), QUERY_DIR3)
    index_dir = os.path.join(os.getcwd(), INDEX_DIR)
    ms = MUSEUM(host=ES_HOST, port=ES_PORT, use_caching=False)
    lists_in = os.listdir(index_dir)
    lists_ = os.listdir(query_dir)
    ssdeep_time = []

    for query_file in lists_ :
        path = os.path.join(query_dir, query_file)
        a = ssdeep.hash_from_file(path)
        x = time.time()
        result = ms.search(INDEX, path, limit=50)
        result_time = time.time() - x
        vi_list = []
        for hit in result['hits']:
            vi_list.append(hit['file_name'])

        x = time.time()
        for f_ in vi_list:
            index_path = os.path.join(index_dir, f_)
            b = ssdeep.hash_from_file(index_path)
            result_ssdeep = ssdeep.compare(a, b)
        ssdeep_mean = time.time() - x
        if ssdeep_mean / result_time < 3 :
            print(query_file)
def ex3_ex() :
    ff_list = []
    query_dir2 = os.path.join(os.getcwd(), QUERY_DIR2)
    index_dir = os.path.join(os.getcwd(), INDEX_DIR)
    ms = MUSEUM(host=ES_HOST, port=ES_PORT, use_caching=False)
    lists_in = os.listdir(index_dir)
    lists_ = os.listdir(query_dir2)
    for fff in lists_:

        path = os.path.join(query_dir2, fff)
        result = ms.search(INDEX, path, limit=50)
        if len(result['hits']) == 1 :
            ff_list.append(fff)
    print(ff_list)
    print(len(ff_list))
def ex3() :
    ff_list = []
    query_dir2 = os.path.join(os.getcwd(), QUERY_DIR2)
    index_dir = os.path.join(os.getcwd(), INDEX_DIR)
    ms = MUSEUM(host=ES_HOST, port=ES_PORT, use_caching=False)
    lists_in = os.listdir(index_dir)
    lists_ = os.listdir(query_dir2)
    for fff in lists_:

        path = os.path.join(query_dir2, fff)
        result = ms.search(INDEX, path, limit=50)
        for hit in result['hits']:
            if hit['estimated_similarity'] == 0:
                ff_list.append(fff)
                break
    for fff in ff_list:
        os.remove(os.path.join(query_dir2, fff))
    print(ff_list)
    print(len(ff_list))
def ex1() :
    ex_list = []
    query_dir = os.path.join(os.getcwd(), QUERY_DIR1)
    ms = MUSEUM(host=ES_HOST, port=ES_PORT, use_caching=False)
    lists_ = os.listdir(query_dir)
    x = time.time()
    for query_file in lists_ :
        path = os.path.join(query_dir, query_file)
        result = ms.search(INDEX, path, limit=50)

        for hit in result['hits'][1:]:
            if hit['estimated_similarity']==1 or len(result['hits'])==1 or hit['estimated_similarity']==0 :
                ex_list.append(query_file)
                break
    # for fff in ex_list:
    #     os.remove(os.path.join(query_dir, fff))
    print(ex_list)
    print(len(ex_list))
if __name__=='__main__' :
    ex3_ex()